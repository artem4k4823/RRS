from sqladmin import ModelView
from sqladmin.filters import BooleanFilter, OperationColumnFilter
from app.core.models.user import User
from app.core.models.post import Post
from app.core.models.subscribtion import Subscription
from app.core.models.user import User

class UserAdmin(ModelView, model=User):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = [User.id, User.username, User.password, User.isCreator, User.isAdmin, User.status]
    column_searchable_list = ('username',)
    column_sortable_list = ('id', 'username', 'status')
    column_filters = (BooleanFilter(User.status),)

class PostAdmin(ModelView, model=Post):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = ('id', 'title', 'link', 'summary', 'published_at', 'feed_id', 'user_id', 'is_read', 'is_favorite', 'created_at', 'feed', 'user')
    column_searchable_list = ('title', 'link', 'summary')
    column_sortable_list = ('id', 'published_at', 'created_at')
    column_filters = (BooleanFilter(Post.is_read), BooleanFilter(Post.is_favorite))

class SubscriptionAdmin(ModelView, model=Subscription):
    can_create = True
    can_edit = True
    can_delete = True
    can_view_details = True
    column_list = ('id', 'feed_url', 'user_id', 'user', 'posts')
    column_searchable_list = ('feed_url',)
    column_sortable_list = ('id', 'user_id')
    column_filters = (OperationColumnFilter(Subscription.user_id),)