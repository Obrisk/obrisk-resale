

# Signal to save each new blog post instance into ElasticSearch
#@receiver(post_save, sender=Classified)
#def index_post(sender, instance, **kwargs):
    #instance.indexing()