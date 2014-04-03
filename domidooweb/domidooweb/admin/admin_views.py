import uuid
import os.path

from pyramid.httpexceptions import HTTPFound
from pyramid.view import view_config
from domidooweb.domain import ImageRepository

from domidooweb.models.image import Image
from domidooweb.models.place import Place
from domidooweb.models.base import DBSession
from domidooweb.models.place_repository import PlaceRepository
from domidooweb.models.tag_repository import TagRepository


def save_uploaded_file(form_field, upload_dir):
    input_file = form_field.file
    original_filename = form_field.filename
    the_name = "%s.%s" %( uuid.uuid4(), os.path.basename(original_filename) )
    file_path = os.path.join(upload_dir, the_name)

    temp_file_path = file_path + '~'
    
    output_file = open(temp_file_path, 'wb')

    input_file.seek(0)
    while True:
        data = input_file.read(2<<16)
        if not data:
            break
        output_file.write(data)

    output_file.close()

    os.rename(temp_file_path, file_path)
    
    return the_name







@view_config(route_name='admin.home', renderer='admin/home.mak')
def admin_home(request):
    return {}


@view_config(route_name='admin.places.new', renderer='admin/places_new.mak')
def place_new(request):
    if(request.method == 'GET'):
        return {'error': '', 'name': '', 'city': ''}
    else:
        dat = request.POST
        name = dat.get('name')
        city = dat.get('city')
        image = dat.get('image')

        upload_dir = request.registry.settings['images.uploaded']
        if hasattr(image, 'filename'):
            image_filename = save_uploaded_file(request.POST['image'], upload_dir)
        else:
            image_filename = None

        place = Place(name=name, city=city)
        place.images.append(Image(image_filename, place))
        DBSession.add(place)

        return HTTPFound(location = request.route_url('admin.places.new'))


@view_config(route_name='admin.tags.new', renderer='admin/tags_new.mak')
def tags_new(request):
    if(request.method == 'GET'):
        return {'error': '', 'name': ''}
    else:
        dat = request.POST
        name = dat.get('name')
        
        tag = TagRepository().get_or_create_by_name(name)
        DBSession.add(tag)

        return HTTPFound(location = request.route_url('admin.tags.new'))

@view_config(route_name='admin.tags.add', renderer='json')
def tags_add(request):
    place_id = request.POST.get('place')
    tag_name = request.POST.get('tag')

    place = PlaceRepository().get(place_id)
    tag = TagRepository().get_or_create_by_name(tag_name)
    
    place.tags.append(tag)

    return {'result': 'ok'}


@view_config(route_name='admin.places', renderer='json')
def places(request):
    return {'places': [ p.to_json() for p in PlaceRepository().get_all() ] }


@view_config(route_name='admin.tags', renderer='json')
def tags(request):
    return {'tags': [ tag.to_json() for tag in TagRepository().get_all() ] }


@view_config(route_name='admin.images.get', renderer='json')
def images_get(request):

    image_id = request.matchdict['id']
    image = ImageRepository().get(image_id)
    return {'image': image.to_json()}

