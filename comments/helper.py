from django.core.cache import cache

from common import rds
from post.models import Post


def page_cache(timeout):
    '''页面缓存'''
    def deco(view_func):
        def wrapper(request):
            key = 'PageCache-%s-%s' % (request.session.session_key, request.get_full_path())
            response = cache.get(key)
            print('get from cache: %s' % response)
            if response is None:
                response = view_func(request)
                print('get from view: %s' % response)
                cache.set(key, response, timeout)
                print('set to cache')
            return response
        return wrapper
    return deco


def read_counter(read_view):
    '''帖子阅读计数装饰器'''
    def wrapper(request):
        response = read_view(request)
        # 状态码为 200 时进行计数
        if response.status_code == 200:
            post_id = int(request.GET.get('post_id'))
            rds.zincrby('ReadRank', post_id)
        return response
    return wrapper


def get_top_n(num):

    ori_data = rds.zrevrange('ReadRank', 0, num - 1, withscores=True)

    cleaned = [[int(post_id), int(count)] for post_id, count in ori_data]

    # 方法二
    post_id_list = [post_id for post_id, _ in cleaned]  
    posts = Post.objects.filter(id__in=post_id_list)   
    posts = sorted(posts, key=lambda post: post_id_list.index(post.id))  
    for post, item in zip(posts, cleaned):
        item[0] = post  
    return cleaned
