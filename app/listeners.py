from . import db
from .models import Post

# Registering db listeners
db.event.listen(Post.body, 'set', Post.on_changed_body)
