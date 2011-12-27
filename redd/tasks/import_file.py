#!/usr/bin/env python

from datetime import datetime

from celery.contrib.abortable import AbortableTask
from django.conf import settings

from redd import solr

SOLR_ADD_BUFFER_SIZE = 500

class ImportFileTask(AbortableTask):
    """
    Base type for file import tasks. 
    """
    abstract = True

    # All subclasses should be within this namespace
    name = 'redd.tasks.import'

    def task_start(self, task_status, message):
        """
        Mark that task has begun.
        """
        task_status.status = 'STARTED' 
        task_status.start = datetime.now()
        task_status.message = message 
        task_status.save()

    def task_update(self, task_status, message):
        """
        Update task status message.
        """
        task_status.message = message 
        task_status.save()

    def task_abort(self, task_status, message):
        """
        Mark that task has aborted.
        """
        task_status.status = 'ABORTED'
        task_status.end = datetime.now()
        task_status.message = message
        task_status.save()

    def task_complete(self, task_status, message):
        """
        Mark that task has completed.
        """
        task_status.status = 'SUCCESS'
        task_status.end = datetime.now()
        task_status.message = message
        task_status.save()

    def task_exception(self, task_status, message, formatted_traceback):
        """
        Mark that task raised an exception
        """
        task_status.status = 'FAILURE'
        task_status.message = message 
        task_status.traceback = formatted_traceback
        task_status.save()

    def run(self, dataset_slug, *args, **kwargs):
        """
        Execute import.
        """
        raise NotImplementedError() 

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        """
        Save final status, results, etc.
        """
        from redd.models import Dataset, Notification
        
        dataset = Dataset.objects.get(slug=args[0])
        task_status = dataset.current_task 

        notification = Notification(
            recipient=dataset.creator,
            related_task=task_status,
            related_dataset=dataset
        )

        if einfo:
            self.task_exception(
                task_status,
                'Import failed',
                u'\n'.join([einfo.traceback, unicode(retval)])
            )
            
            notification.message = 'Import of %s failed' % dataset.name
            notification.type = 'error'
        else:
            self.task_complete(task_status, 'Import complete')
            
            notification.message = 'Import of <strong>%s</strong> complete' % dataset.name
        
        notification.save()

        # If import failed, clear any data that might be staged
        if task_status.status == 'FAILURE':
            solr.delete(settings.SOLR_DATA_CORE, 'dataset_slug:%s' % args[0], commit=True)
