#!/usr/bin/env python2
# -*- coding: utf-8 -*-


def add_starter(chat_id):
    with open('starters.txt', 'a') as db_start:
        db_start.write(str(chat_id) + '\n')
    return None


def get_starters():
    with open('starters.txt', 'r') as db_start:
        ids = db_start.read().splitlines()
    res = []
    for single_id in ids:
        res.append(int(single_id))
    return res


def add_admins():
    result = []
    with open('admin_ids', 'r') as admins:
        for chat_id in admins.read().splitlines():
            result.append(int(chat_id))
    return result


def get_subscribers():
    with open('subscribers.txt', 'r') as db:
        ids = db.read().splitlines()
    res = []
    for sub_id in ids:
        res.append(int(sub_id))
    return res


def add_subscriber(chat_id):
    with open('subscribers.txt', 'a') as db_sub:
        db_sub.write(str(chat_id) + '\n')
    return None


def del_subscriber(chat_id):
    with open('subscribers.txt', 'r') as db_sub:
        subscribers = db_sub.read().splitlines()
        subscribers.remove(str(chat_id))
    with open('subscribers.txt', 'w') as db_sub:
        db_sub.write('\n'.join(subscribers) + '\n')
    return None

# TEST SUBS RELATED FUNCTIONS


def get_testsubs():
    with open('testsubs.txt', 'r') as db:
        ids = db.read().splitlines()
    res = []
    for sub_id in ids:
        res.append(int(sub_id))
    return res


def add_testsub(chat_id):
    with open('testsubs.txt', 'a') as db_sub:
        db_sub.write(str(chat_id) + '\n')
    return None


def del_testsub(chat_id):
    with open('testsubs.txt', 'r') as db_sub:
        testsubs = db_sub.read().splitlines()
        testsubs.remove(str(chat_id))
    with open('testsubs.txt', 'w') as db_sub:
        db_sub.write('\n'.join(testsubs) + '\n')
    return None


def get_suspects():
    with open('suspects.txt', 'r') as db_sub:
        ids = db_sub.read().splitlines()
    res = []
    for sub_id in ids:
        res.append(int(sub_id))
    return res


def check_suspect(suspect_id):
    with open('suspects.txt', 'r') as db_sub:
        suspects = db_sub.read().splitlines()
        suspects.append(str(suspect_id))
        if (sum(1 for i in get_suspects() if i == suspect_id)) > 5:
            suspects = [id for id in suspects if id != str(suspect_id)]
            del_subscriber(suspect_id)
    with open('suspects.txt', 'w') as db_sub:
        db_sub.write('\n'.join(suspects[-100:]) + '\n')
    return None
