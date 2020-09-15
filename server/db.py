from sqlalchemy import (
    MetaData, Table, Column,
    Integer, Boolean, create_engine
)

import os

meta = MetaData()

subscribers = Table(
    'subscribes_base', meta,
    Column('chat_id', Integer, primary_key=True),
    Column('subscribed', Boolean, index=True)
)


async def init_db(app):
    url = os.environ.get('DATABASE_URL')
    engine = create_engine(url, echo=True)
    app['db'] = engine


def add_subscriber(engine, chat_id,  state=True):
    with engine.connect() as conn:
        expression = subscribers.insert()
        result = conn.execute(expression, [{'chat_id': chat_id, 'subscribed': state}])


def check_subscriber_exist(engine, chat_id):
    """
    check if record with chat_id exist, return it, otherwise return None
    """
    with engine.connect() as conn:
        expression = subscribers.select(subscribers).where(subscribers.c.chat_id == chat_id)
        result = conn.execute(expression)

        if result.rowcount:
            return result.next()
        else:
            return None


def change_state_subscriber(engine, chat_id, state=True):

    with engine.connect() as conn:
        expression = subscribers.update().where(subscribers.c.chat_id == chat_id).values(subscribed=state)
        result = conn.execute(expression)
        return result.rowcount


def get_all_subscriber(engine, state=True):
    """
    return list of subscriber's chat_id with specified state
    """
    with engine.connect() as conn:
        expression = subscribers.select(subscribers).where(subscribers.c.subscribed == state)
        result = conn.execute(expression)

        subscribesr_list = list()
        for item in result:
            subscribesr_list.append(item[0])
        return subscribesr_list


def delete_subscriber(engine, chat_id):

    with engine.connect() as conn:
        expression = subscribers.delete(subscribers).where(subscribers.c.chat_id == chat_id)
        result = conn.execute(expression)

        return result.rowcount


def smart_change_subscriber(engine, chat_id,  state=True):

    """
    check if chat id in db, and add record or change it's state, if necessary
    """

    check = check_subscriber_exist(engine, chat_id)

    if check:
        if check[1] != state:
            change_state_subscriber(engine, chat_id, state=state)
            return 1
        else:
            return 0
    else:
        add_subscriber(engine, chat_id, state=state)
        return 2



