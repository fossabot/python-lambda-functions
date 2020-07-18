import os
from uuid import uuid4
from sqlalchemy.orm import relationship, backref, sessionmaker
from sqlalchemy import create_engine
from crud.model import *
from datetime import datetime
import numpy


def get_db_session():
    """Returns a DB session

    Returns
    ------
    db: DB Connection
        The database connection
    """

    # TODO Environment variables, put db session in seperate class
    cluster_arn = "arn:aws:rds:eu-central-1:891514678401:cluster:serverless-db"
    secret_arn = "arn:aws:secretsmanager:eu-central-1:891514678401:secret:ServerlessDBSecret-7oczW5"

    database_name = os.environ['DBNAME']

    db = create_engine('mysql+auroradataapi://:@/{0}'.format(database_name),
                       echo=True,
                       connect_args=dict(aurora_cluster_arn=cluster_arn, secret_arn=secret_arn))

    Session = sessionmaker(bind=db)
    session = Session()

    return session


def create_item_db(item):
    """Inserts a new item into the database

    Parameters
    ----------
    item: Item, required
        The item to be inserted

    Returns
    ------
    item: Item
        The inserted item
    """

    session = get_db_session()

    item.id = str(uuid4())
    item.status = "new"
    item.open_reviews = 3
    session.add(item)
    session.commit()

    return item


def update_object_db(obj):
    """Updates an existing item in the database

    Parameters
    ----------
    obj: object to be merged in the DB, required
        The item to be updates

    Returns
    ------
    obj: The merged object
    """

    session = get_db_session()

    session.merge(obj)
    session.commit()

    return obj


def get_all_items_db():
    """Returns all items from the database

    Returns
    ------
    items: Item[]
        The items
    """

    session = get_db_session()
    items = session.query(Item).all()
    return items


def get_item_by_content_db(content):
    """Returns an item with the specified content from the database

        Returns
        ------
        item: Item
            The item
        Null, if no item was found
        """
    session = get_db_session()
    item = session.query(Item).filter(Item.content == content).first()
    if item is None:
        raise Exception("No item found.")
    return item


def create_submission_db(submission):
    """Inserts a new submission into the database

    Parameters
    ----------
    submission: Submission, required
        The submission to be inserted

    Returns
    ------
    submission: Submission
        The inserted submission
    """
    session = get_db_session()

    submission.id = str(uuid4())
    submission.submission_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    session.add(submission)
    session.commit()

    return submission


def get_all_submissions_db():

    session = get_db_session()
    submissions = session.query(Submission).all()
    return submissions


def create_user_db(user):
    """Inserts a new user into the database

    Parameters
    ----------
    user: User, required
        The user to be inserted

    Returns
    ------
    user: User
        The inserted user
    """

    session = get_db_session()

    user.score = 0
    user.level = 1
    user.experience_points = 0
    session.add(user)
    session.commit()

    return user


def get_all_users_db():
    """Returns all users from the database

    Returns
    ------
    users: User[]
        The users
    """

    session = get_db_session()
    users = session.query(User).all()
    return users


def create_review_db(review):
    """Inserts a new review into the database

    Parameters
    ----------
    review: Review, required
        The review to be inserted

    Returns
    ------
    review: Review
        The inserted review
    """

    session = get_db_session()

    review.id = str(uuid4())
    session.add(review)
    session.commit()

    return review


def get_all_reviews_db():
    """Returns all reviews from the database

    Returns
    ------
    reviews: Review[]
        The reviews
    """

    session = get_db_session()
    reviews = session.query(Review).all()
    return reviews

def get_reviews_by_item_id(item_id):

    session = get_db_session()
    reviews = session.query(Review).filter(Review.item_id == item_id)
    return reviews

def get_review_by_peer_review_id_db(peer_review_id):
    """Returns a review from the database with the specified peer review id
    
    Parameters
    ----------
    peer_review_id: Str, required
        The peer review id to query for

    Returns
    ------
    review: Review
        The review
    """

    session = get_db_session()
    review = session.query(Review).filter(Review.peer_review_id == peer_review_id).first()
    return review


def create_review_answer_db(review_answer):
    """Inserts a new review answer into the database

    Parameters
    ----------
    review_answer: ReviewAnswer, required
        The review answer to be inserted

    Returns
    ------
    review_answer: reviewAnswer
        The inserted review answer
    """

    session = get_db_session()

    review_answer.id = str(uuid4())
    session.add(review_answer)
    session.commit()

    return review_answer

def create_review_answer_set_db(review_answers):
    session = get_db_session()
    for review_answer in review_answers:
        review_answer.id = str(uuid4())
        session.add(review_answer)    
    session.commit()


def get_all_review_answers_db():
    """Returns all review answers from the database

    Returns
    ------
    review_answers: ReviewAnswer[]
        The review answers
    """

    session = get_db_session()
    review_answers = session.query(ReviewAnswer).all()
    return review_answers

def get_review_answers_by_review_id_db(review_id):
    """Returns all review answers from the database that belong to the specified review

    Returns
    ------
    review_answers: ReviewAnswer[]
        The review answers
    """

    session = get_db_session()
    review_answers = session.query(ReviewAnswer).filter(ReviewAnswer.review_id == review_id)
    return review_answers


def get_all_review_questions_db():
    """Returns all review answers from the database

    Returns
    ------
    review_questions: ReviewQuestion[]
        The review questions
    """

    session = get_db_session()
    review_questions = session.query(ReviewQuestion).all()
    return review_questions


def get_user_by_id(id):
    """Returns a user by their id
    Parameters
    ----------
    id: str, required
        The id of the user
    Returns
    ------
    user: User
        The user
    """

    session = get_db_session()
    user = session.query(User).get(id)
    return user

def get_item_by_id(id):
    """Returns an item by its id
    Parameters
    ----------
    id: str, required
        The id of the item
    Returns
    ------
    item: Item
        The item
    """

    session = get_db_session()
    item = session.query(Item).get(id)
    return item

def give_experience_point(user_id):    
    user = get_user_by_id(user_id)
    user.experience_points = user.experience_points + 1
    if user.experience_points >= 5:
        user.level = 2
    update_object_db(user)

def check_if_review_still_needed(item_id, is_peer_review):
    item = get_item_by_id(item_id)
    status = item.status
    if is_peer_review == True:
        if status == "needs_senior":
            return True
        else:
            return False
    if is_peer_review == False:
        if status == "needs_junior":
            return True
        else:
            return False

def close_open_junior_review(item_id, peer_review_id):
    """Returns all reviews from the database that belong to the item with the specified id
    
    Parameters
    ----------
    item_id: Str, required
        The item id to query for
    
    Returns
    ------
    review: Review
        The open junior review
    """
    session = get_db_session()
    query_result = session.query(Review).filter(
        Review.item_id == item_id,
        Review.is_peer_review == "false",
        Review.peer_review_id == None
        )
    if query_result.is_single_entity == False:
        raise Exception("Error! Either no or too many open junior reviews found!")    
    open_junior_review = query_result.one()
    open_junior_review.peer_review_id = peer_review_id
    update_object_db(open_junior_review)

def get_pair_variance(review_id):
    junior_review = get_review_by_peer_review_id_db(review_id)
    peer_review_answers = get_review_answers_by_review_id_db(review_id)
    junior_review_answers = get_review_answers_by_review_id_db(junior_review.id)

    junior_review_score_sum = 0
    peer_review_score_sum = 0

    for answer in junior_review_answers:
        junior_review_score_sum = junior_review_score_sum + answer.answer

    for answer in peer_review_answers:
        peer_review_score_sum = peer_review_score_sum + answer.answer
    
    junior_review_average = junior_review_score_sum / junior_review_answers.count()
    peer_review_average = peer_review_score_sum / peer_review_answers.count()

    variance = numpy.var([junior_review_average, peer_review_average])
    return variance

def compute_item_result_score(item_id):
    total_answer_sum = 0
    counter = 0
    reviews = get_reviews_by_item_id(item_id)
    for review in reviews:
        answers = get_review_answers_by_review_id_db(review.id)
        for answer in answers:
            counter = counter + 1
            total_answer_sum = total_answer_sum + answer.answer
    result = total_answer_sum / counter
    return result
