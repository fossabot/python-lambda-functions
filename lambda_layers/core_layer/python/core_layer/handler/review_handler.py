from uuid import uuid4
import random
from sqlalchemy import or_
from sqlalchemy.orm import sessionmaker
from core_layer.connection_handler import get_db_session, update_object
from core_layer import helper
from core_layer.model.review_model import Review
from core_layer.model.review_pair_model import ReviewPair
from core_layer.model.review_answer_model import ReviewAnswer
from core_layer.handler import item_handler
from core_layer.handler import review_question_handler, user_handler, review_pair_handler, review_answer_handler


def get_review_by_id(review_id, is_test, session) -> Review:
    session = get_db_session(is_test, session)

    review = session.query(Review).filter(
        Review.id == review_id
    ).one()

    return review


def get_partner_review(review, is_test, session) -> Review:
    session = get_db_session(is_test, session)

    pair = session.query(ReviewPair).filter(or_(ReviewPair.junior_review_id ==
                                                review.id, ReviewPair.senior_review_id == review.id)) \
        .first()

    try:
        if review.id == pair.junior_review_id:
            return get_review_by_id(pair.senior_review_id, is_test, session)

        if review.id == pair.senior_review_id:
            return get_review_by_id(pair.junior_review_id, is_test, session)
    except:
        return None


def create_review(user, item, is_test, session) -> Review:
    """Accepts an item for review

    Parameters
    ----------
    user: User
        The user that reviews the item
    item: Item
        The item to be reviewed by the user

    Returns
    ------
    item: Item
        The case to be assigned to the user
    """
    # If a ReviewInProgress exists for the user, return
    session = get_db_session(is_test, session)

    try:
        review = session.query(Review).filter(
            Review.user_id == user.id, Review.status == "in_progress", Review.item_id == item.id).one()
        return review
    except:
        pass

    # If the amount of reviews in progress equals the amount of reviews needed, raise an error
    if item.in_progress_reviews_level_1 >= item.open_reviews_level_1:
        if user.level_id > 1:
            if item.in_progress_reviews_level_2 >= item.open_reviews_level_2:
                raise Exception(
                    'Item cannot be accepted since enough other detecitves are already working on the case')
        else:
            raise Exception(
                'Item cannot be accepted since enough other detecitves are already working on the case')
    # Create a new ReviewInProgress
    rip = Review()
    rip.id = str(uuid4())
    rip.item_id = item.id
    rip.user_id = user.id
    rip.start_timestamp = helper.get_date_time_now(is_test)
    rip.status = "in_progress"
    session.add(rip)
    session.commit()

    # If a user is a senior, the review will by default be a senior review,
    # except if no senior reviews are needed
    if user.level_id > 1 and item.open_reviews_level_2 > item.in_progress_reviews_level_2:
        rip.is_peer_review = True
        item.in_progress_reviews_level_2 = item.in_progress_reviews_level_2 + 1

        # Check if a pair with open senior review exists
        pair_found = False
        for pair in item.review_pairs:
            if pair.senior_review_id == None:
                pair.senior_review_id = rip.id
                pair_found = True
                session.merge(pair)
                break

        # Create new pair, if review cannot be attached to existing pair
        if pair_found == False:
            pair = ReviewPair()
            pair.id = str(uuid4())
            pair.senior_review_id = rip.id
            item.review_pairs.append(pair)
            session.merge(pair)

    # If review is junior review
    else:
        rip.is_peer_review = False
        item.in_progress_reviews_level_1 = item.in_progress_reviews_level_1 + 1

        # Check if a pair with open junior review exists
        pair_found = False
        for pair in item.review_pairs:
            if pair.junior_review_id == None:
                pair.junior_review_id = rip.id
                pair_found = True
                session.merge(pair)
                break

        # Create new pair, if review cannot be attached to existing pair
        if pair_found == False:
            pair = ReviewPair()
            pair.id = str(uuid4())
            pair.junior_review_id = rip.id
            item.review_pairs.append(pair)
            session.merge(pair)

    session.merge(rip)
    session.merge(item)
    session.commit()
    rip = create_answers_for_review(rip, is_test, session)
    return rip


def compute_review_result(review_answers):
    if(review_answers == None):
        raise TypeError('ReviewAnswers is None!')

    if not isinstance(review_answers, list):
        raise TypeError('ReviewAnswers is not a list')

    if(len(review_answers) <= 0):
        raise ValueError('ReviewAnswers is an empty list')

    answers = [
        review_answer.answer for review_answer in review_answers if review_answer.answer is not None]

    answers = [answer for answer in answers if answer > 0]

    return sum(answers) / len(answers)


def get_old_reviews_in_progress(is_test, session):
    old_time = helper.get_date_time_one_hour_ago(is_test)
    session = get_db_session(is_test, session)
    rips = session.query(Review).filter(
        Review.start_timestamp < old_time, Review.status == "in_progress").all()
    return rips


def delete_old_reviews_in_progress(rips, is_test, session):
    for rip in rips:
        item = item_handler.get_item_by_id(rip.item_id, is_test, session)
        if rip.is_peer_review == True:
            item.in_progress_reviews_level_2 -= 1
        else:
            item.in_progress_reviews_level_1 -= 1
        session.merge(item)
        session.delete(rip)
    session.commit()


def create_answers_for_review(review: Review, is_test, session):
    partner_review = get_partner_review(review, is_test, session)
    if partner_review != None:
        for partner_answer in partner_review.review_answers:
            if partner_answer.review_question is not None:
                answer = ReviewAnswer()
                answer.id = str(uuid4())
                answer.review_question = partner_answer.review_question
                answer.review = review
                session.add(answer)
    else:
        item_type_id = review.item.item_type_id
        questions = review_question_handler.get_all_parent_questions(
            item_type_id, is_test, session)
        random.shuffle(questions)
        for question in questions[:6]:
            answer = ReviewAnswer()
            answer.id = str(uuid4())
            answer.review_question = question
            answer.review = review
            session.add(answer)
            if question.max_children > 0:
                child_questions = review_question_handler.get_all_child_questions(
                    question.id, True, session)
                for child_question in child_questions:
                    answer = ReviewAnswer()
                    answer.id = str(uuid4())
                    answer.review_question = child_question
                    answer.review = review
                    session.add(answer)

    session.commit()
    session.refresh(review)
    return review


def close_review(review: Review, is_test, session) -> Review:
    review.status = "closed"
    review.finish_timestamp = helper.get_date_time_now(is_test)
    user_handler.give_experience_point(
        review.user_id, is_test, session)

    pair = review_pair_handler.get_review_pair_from_review(
        review, is_test, session)
    partner_review = get_partner_review(
        review, is_test, session)

    if partner_review != None and partner_review.status == 'closed':
        pair.is_good = True
        for answer in review.review_answers:
            partner_answer = review_answer_handler.get_partner_answer(
                partner_review, answer.review_question_id, is_test, session)
            if (answer.answer == None and partner_answer.answer != None) or (answer.answer != None and partner_answer.answer == None):
                pair.is_good = False
            elif (answer.answer == 0 and partner_answer.answer != 0) or (answer.answer != 0 and partner_answer.answer == 0):
                pair.is_good = False

        if pair.is_good:
            difference = review_pair_handler.compute_difference(pair)
            pair.variance = difference
            pair.is_good = True if difference <= 1 else False

        review.item.in_progress_reviews_level_1 -= 1
        review.item.in_progress_reviews_level_2 -= 1
        if pair.is_good:
            review.item.open_reviews -= 1
            review.item.open_reviews_level_1 -= 1
            review.item.open_reviews_level_2 -= 1

        pairs = review_pair_handler.get_review_pairs_by_item(
            pair.item_id, is_test, session)

        if(len(list(filter(lambda p: p.is_good, pairs))) >= 4):
            review.item.status = "closed"
            review.item.close_timestamp = review.finish_timestamp
            review.item.result_score = item_handler.compute_item_result_score(
                review.item_id, is_test, session)

    update_object(review, is_test, session)
    update_object(pair, is_test, session)
    update_object(review.item, is_test, session)

    return review
