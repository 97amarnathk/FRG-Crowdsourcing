# -*- coding: utf8 -*-
# This file is part of PYBOSSA.
#
# Copyright (C) 2015 Scifabric LTD.
#
# PYBOSSA is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PYBOSSA is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with PYBOSSA.  If not, see <http://www.gnu.org/licenses/>.
"""Scheduler module for PYBOSSA tasks."""
from sqlalchemy.sql import func, desc
from sqlalchemy import and_
from pybossa.model import DomainObject
from pybossa.model.task import Task
from pybossa.model.task_run import TaskRun
from pybossa.model.counter import Counter
from pybossa.core import db
import random
from pybossa.util import (Pagination, admin_required, get_user_id_or_ip, rank,
                          handle_content_type, redirect_content_type,
                          get_avatar_url)
from flask import url_for
session = db.slave_session
from pybossa.core import project_repo,user_repo
from pybossa.model.user import User
from flask.ext.login import login_required, current_user

def new_task(project_id, sched, user_id=None, user_ip=None,
             external_uid=None, offset=0, limit=1, orderby='priority_0', desc=True):
    """Get a new task by calling the appropriate scheduler function."""
    sched_map = {
        'default': get_depth_first_task,
        'breadth_first': get_breadth_first_task,
        'depth_first': get_depth_first_task,
        'incremental': get_incremental_task,
        'FRG':get_frg_task
        }
    scheduler = sched_map.get(sched, sched_map['default'])
    return scheduler(project_id, user_id, user_ip, external_uid, offset=offset, limit=limit, orderby=orderby, desc=desc)

def get_frjsg_task(#project_id, user_id=None, user_ip=None, n_answers=30, offset=0):
	project_id, user_id=None, user_ip=None,
	                         external_uid=None, offset=0, limit=1,
	                         orderby='priority_0', desc=True):
    """Return a random task for the user."""
    print "Hello FRG"

    project = project_repo.get(project_id)
    if project and len(project.tasks) > 0:
        return project.tasks[0:1]
    else:
        return None


def get_frg_task(#project_id, user_id=None, user_ip=None, n_answers=30, offset=0):
	project_id, user_id=None, user_ip=None,
	                         external_uid=None, offset=0, limit=1,
	                         orderby='priority_0', desc=True):
	project = project_repo.get(project_id)
	"""Get all available tasks for a given project and user."""
	data = None
	print offset
	print "offset"
        print offset
	if user_id and not user_ip and not external_uid:
		subquery = session.query(TaskRun.task_id).filter_by(project_id=project_id, user_id=user_id)
	else:
		 if not user_ip:
		 	 user_ip = '127.0.0.1'
		 if user_ip and not external_uid:
		 	subquery = session.query(TaskRun.task_id).filter_by(project_id=project_id, user_ip=user_ip)
		 else:
		 	subquery = session.query(TaskRun.task_id).filter_by(project_id=project_id, external_uid=external_uid)

	query = session.query(Task).filter(and_(~Task.id.in_(subquery.subquery()),
                                            Task.project_id == project_id,Task.state != 'completed'))
       
	dictobj={"images":[],"videos":[],"documents":[],"audios":[]}

	for q in query:
		if q.info["type"]=="images":
			dictobj["images"].append(q)
		elif q.info["type"]=="documents":
			dictobj["documents"].append(q)
		elif q.info["type"]=="videos":
			dictobj["videos"].append(q)
		elif q.info["type"]=="audios":
			dictobj["audios"].append(q)
	print dictobj
	if project and len(project.tasks)>0:
		user_obj=session.query(User).filter_by(id=current_user.id).first()
		x=user_obj.info["score"][0]
		x=None
		for i in user_obj.info["score"]:
			print i["project_id"]
			print project.id
			if(i["project_id"]==project.id):
				x=i
		image_score=x["image_score"]
		video_score=x["video_score"]
		audio_score=x["audio_score"]
		document_score=x["document_score"]
		dict_score={"images":image_score,"videos":video_score,"audios":audio_score,"documents":document_score}
		print dict_score
		for key, value in dictobj.iteritems():
		    if(len(dictobj[key])==0):
		        dict_score.pop(key, None)
		sort_dict=sorted(dict_score.items(),key = lambda t:t[1])
		print sort_dict
		top_score=[]
		files_list=[]
		if(len(sort_dict)==1):
			top_score.extend(dictobj[sort_dict[0][0]])
			files_list.extend(sort_dict[0][0]);
		else:
			print "here"
			top_score.extend(dictobj[sort_dict[len(sort_dict)-1][0]])
			files_list.append(sort_dict[len(sort_dict)-1][0]);
			top_score.extend(dictobj[sort_dict[len(sort_dict)-2][0]])
			files_list.append(sort_dict[len(sort_dict)-2][0]);
		print top_score
		li=[]
		noli=[]
		for i in top_score:
			print i.id
			li.extend([i.id])
		
		#query=session.query(Task).filter(Task.id==li[0])
		query=session.query(Task).filter(Task.id.in_(li),Task.task_type.in_(files_list))
		print top_score;
		print "this"
		print query
		data= query.limit(limit).offset(offset).all()
		return _handle_tuples(data)
		#return None
	else:
		return None



def get_breadth_first_task(project_id, user_id=None, user_ip=None,
                           external_uid=None, offset=0, limit=1, orderby='id', desc=False):
    """Get a new task which have the least number of task runs."""
    project_query = session.query(Task.id).filter(Task.project_id==project_id,
                                                  Task.state!='completed')
    if user_id and not user_ip and not external_uid:
        subquery = session.query(TaskRun.task_id).filter_by(project_id=project_id,
                                                            user_id=user_id)
    else:
        if not user_ip:  # pragma: no cover
            user_ip = '127.0.0.1'
        if user_ip and not external_uid:
            subquery = session.query(TaskRun.task_id).filter_by(project_id=project_id,
                                                                user_ip=user_ip)
        else:
            subquery = session.query(TaskRun.task_id).filter_by(project_id=project_id,
                                                                external_uid=external_uid)

    tmp = project_query.except_(subquery)
    query = session.query(Task, func.sum(Counter.n_task_runs).label('n_task_runs'))\
                   .filter(Task.id==Counter.task_id)\
                   .filter(Counter.task_id.in_(tmp))\
                   .group_by(Task.id)\
                   .order_by('n_task_runs ASC')\

    query = _set_orderby_desc(query, orderby, desc)
    print offset
    print "breadth_first"
    data = query.limit(limit).offset(offset).all()
    return data


def get_depth_first_task(project_id, user_id=None, user_ip=None,
                         external_uid=None, offset=0, limit=1,
                         orderby='priority_0', desc=True):
    """Get a new task for a given project."""
    tasks = get_candidate_task_ids(project_id, user_id,
                                   user_ip, external_uid, limit, offset,
                                   orderby=orderby, desc=desc)
    print "hii in depth"
    print offset
    print "this is limit"
    print limit
    return tasks


def get_incremental_task(project_id, user_id=None, user_ip=None,
                         external_uid=None, offset=0, limit=1, orderby='id', desc=False):
    """Get a new task for a given project with its last given answer.

    It is an important strategy when dealing with large tasks, as
    transcriptions.
    """
    candidate_tasks = get_candidate_task_ids(project_id, user_id, user_ip,
                                                external_uid, limit, offset,
                                                orderby='priority_0', desc=True)
    total_remaining = len(candidate_tasks)
    if total_remaining == 0:
        return None
    rand = random.randrange(0, total_remaining)
    task = candidate_tasks[rand]
    # Find last answer for the task
    q = session.query(TaskRun)\
        .filter(TaskRun.task_id == task.id)\
        .order_by(TaskRun.finish_time.desc())
    last_task_run = q.first()
    if last_task_run:
        task.info['last_answer'] = last_task_run.info
        # TODO: As discussed in GitHub #53
        # it is necessary to create a lock in the task!
    return [task]


def get_candidate_task_ids(project_id, user_id=None, user_ip=None,
                           external_uid=None, limit=1, offset=0,
                           orderby='priority_0', desc=True):
    """Get all available tasks for a given project and user."""
    data = None
    if user_id and not user_ip and not external_uid:
        subquery = session.query(TaskRun.task_id).filter_by(project_id=project_id, user_id=user_id)
    else:
        if not user_ip:
            user_ip = '127.0.0.1'
        if user_ip and not external_uid:
            subquery = session.query(TaskRun.task_id).filter_by(project_id=project_id, user_ip=user_ip)
        else:
            subquery = session.query(TaskRun.task_id).filter_by(project_id=project_id, external_uid=external_uid)

    query = session.query(Task).filter(and_(~Task.id.in_(subquery.subquery()),
                                            Task.project_id == project_id,
                                            Task.state != 'completed'))
    query = _set_orderby_desc(query, orderby, desc)
    for q in query:
   	print q
    data = query.limit(limit).offset(offset).all()
    return _handle_tuples(data)


def sched_variants():
    return [('default', 'Default'), ('breadth_first', 'Breadth First'),('depth_first', 'Depth First'),('FRG','FRG')]

def _set_orderby_desc(query, orderby, descending):
    """Set order by to query."""
    if orderby == 'fav_user_ids':
        n_favs = func.coalesce(func.array_length(Task.fav_user_ids, 1), 0).label('n_favs')
        query = query.add_column(n_favs)
        if descending:
            query = query.order_by(desc("n_favs"))
        else:
            query = query.order_by("n_favs")
    else:
        if descending:
            query = query.order_by(getattr(Task, orderby).desc())
        else:
            query = query.order_by(getattr(Task, orderby).asc())
    #query = query.order_by(Task.id.asc())
    return query

def _handle_tuples(data):
    """Handle tuples when query returns several columns."""
    tmp = []
    for datum in data:
        if isinstance(datum, DomainObject):
            tmp.append(datum)
        else:
            tmp.append(datum[0])
    return tmp
