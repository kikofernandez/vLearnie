from community.models import EntryCommunityResource, URLCommunityResource, Community, URL, ENTRY,\
    Resource
from django.core.urlresolvers import reverse
from django.http import Http404
from django.db.models import signals
from django.shortcuts import get_object_or_404

def smart_truncate(content, length=100, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return content[:length].rsplit(' ', 1)[0]+suffix

def create_params(instance):
    """
    Parameters for creating the kind of XResource
    """
    excerpt = instance.excerpt
    
    if instance.excerpt == '':
        excerpt = smart_truncate(instance.body, 50)
        
    params = {
                'title': instance.title,
                'author': instance.author,
                'slug': instance.slug,
                'pub_date': instance.pub_date,
                #'type': 1,
                'excerpt': excerpt,
             }
    
    # Parameters that will be used when retrieving the url
    kwargs = {'username':instance.author.username,
              'spacename':instance.space.slug,
              'year': instance.pub_date.year,
              'month': instance.pub_date.strftime("%b").lower(),
              'day': instance.pub_date.day,
              'slug':instance.slug, }
    
    params.update({'url_referrer': reverse('coltrane_entry_detail',kwargs=kwargs)})
    return params

def update_m2m_resource(sender, instance, action, reverse, model, pk_set, **kwargs):
    """
    This method update_m2m_resource, executed after being saved, 
    will try to get the resource if it exist and update the community m2m field.
    If the kind of community resource does not exist, then it will create the object
    and populate the community m2m field. 
    """
    
    if action == 'post_add':
        
        if instance.status:
            accept = False
            
            if (int(instance.status), 'Live') in instance.STATUS_CHOICES:
                accept = True
            print "Accept_post_add: %s" % accept
            
            # If it's not LIVE, then do not update anything. If you tried, it's likely
            # the method create_resource had deleted the object, so it will generate
            # a Http404 exception
            if not accept: return
        
        try:
            # instance.featured means that you want an URLCommunityResource. Otherwise, 
            # create an EntryCommunityResource
            if (instance.featured):
                #query = URLCommunityResource.objects.filter(author=instance.author).filter(slug=instance.slug)
                #kind_community_object = query.get(pub_date=instance.pub_date)
                kind_community_object = get_object_or_404(URLCommunityResource, author=instance.author,
                                                                            slug=instance.slug,
                                                                            pub_date=instance.pub_date)
            else:
                #query = EntryCommunityResource.objects.filter(author=instance.author).filter(slug=instance.slug)
                #kind_community_object = query.get(pub_date=instance.pub_date)
                kind_community_object = get_object_or_404(EntryCommunityResource, author=instance.author,
                                                                            slug=instance.slug,
                                                                            pub_date=instance.pub_date)
            
            #clear resource, otherwise it will keep the older options and the new ones
            kind_community_object.community.clear()
            kind_community_object.save()
            
            # Add the values to the kind of object
            for entry in pk_set:
                kind_community_object.community.add(entry)
            kind_community_object.save()
        except (URLCommunityResource.DoesNotExist, EntryCommunityResource.DoesNotExist, Http404):
            
            # This two lines could be deleted, but for caution's sake
            # we will leave (until further analysis)
            if not accept:
                return
            
            # Creation of the params that will serve to create an instance of
            # cretain kind of resource object
            params = create_params(instance)
            
            # Creation of the kind of object expected
            if instance.featured:
                params['type'] = URL
                kind_community_object = URLCommunityResource.objects.create(**params)
            else:
                params['type'] = ENTRY
                params['body'] = instance.body
                kind_community_object = EntryCommunityResource.objects.create(**params)
            
            # Populate the m2m field
            for entry in pk_set:
                kind_community_object.community.add(entry)
            kind_community_object.save()
 
 
def create_resource(sender, instance, **kwargs):
    """
    This method create_resource will create / update the resource dynamically. Nonetheless, 
    it will not attempt to add any community related object (of the m2m relation) with it,
    since that's the main function of update_m2m_resource.
    """
    if instance.status:
        accept = False
        if (int(instance.status), 'Live') in instance.STATUS_CHOICES:
            accept = True
        #print "Accept: %s" % accept
    
    try:
        params = create_params(instance)
        #print "Instance.featured: %s" % instance.featured
        if (instance.featured):
            #query = URLCommunityResource.objects.filter(author=instance.author).filter(slug=instance.slug)
            #kind_community_object = query.get(pub_date=instance.pub_date)
            kind_community_object = get_object_or_404(URLCommunityResource, author=instance.author,
                                                                            slug=instance.slug,
                                                                            pub_date=instance.pub_date)
            #print "objecto: %s" % kind_community_object
            #print "URL"
        else:
            kind_community_object = get_object_or_404(EntryCommunityResource, author=instance.author,
                                                                              slug=instance.slug,
                                                                              pub_date=instance.pub_date)
            kind_community_object.body = instance.body
            #query = EntryCommunityResource.objects.filter(author=instance.author).filter(slug=instance.slug)
            #kind_community_object = query.get(pub_date=instance.pub_date)
            
            #print "Entry"
            
        if not accept:
            kind_community_object.delete()
            #Resource.objects.filter(slug=instance.slug).filter(author=instance.author).filter(pub_date=instance.pub_date).delete()
            return
        
        kind_community_object.title = instance.title
        kind_community_object.author = instance.author
        kind_community_object.slug = instance.slug
        kind_community_object.pub_date = instance.pub_date
        kind_community_object.url_referrer = params.get('url_referrer')
        
        kind_community_object.save()

    except (URLCommunityResource.DoesNotExist, EntryCommunityResource.DoesNotExist, Http404):
        
        # If the entry is not Live, then it's because is Hidden / Draft, so
        # don't show any of these
        if not accept:
            #print "Return"
            return 
        
        # Creation of the kind of object expected
        if instance.featured:
            params['type'] = URL
            kind_community_object = URLCommunityResource.objects.create(**params)
        else:
            params['type'] = ENTRY
            params['body'] = instance.body
            kind_community_object = EntryCommunityResource.objects.create(**params)
    except TypeError:
        print "Error"
        raise Http404
        