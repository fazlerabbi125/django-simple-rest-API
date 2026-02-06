# django-simple-rest-API

## Create and activate Python virtual environment
- https://docs.python.org/3/library/venv.html
- https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/
- https://code.visualstudio.com/docs/python/environments

Use it for installing packages according to your Python version

## Find and install Python packages:
https://pypi.org/

## Setting up Python version with pyenv:
- https://github.com/pyenv/pyenv
- https://github.com/pyenv-win/pyenv-win

## Using dependency file:
https://www.freecodecamp.org/news/python-requirementstxt-explained/

## .env file usage:
https://dev.to/jakewitcher/using-env-files-for-environment-variables-in-python-applications-55a1

## Generating secret keys
https://docs.python.org/3/library/secrets.html

## Poetry for dependency management
https://python-poetry.org/docs/

## uv for dependency and Python version management
A single tool to replace pip, pip-tools, pipx, poetry, pyenv, twine, virtualenv, and more.

https://docs.astral.sh/uv/getting-started/

## Query optimization of related fields
By default, Django uses Lazy Loading for related objects, and so when you access a related field for the first time, a separate query is executed. Especially if you need to access relational data in a loop, you need query optimization.
- `select_related` - Returns a QuerySet that will “follow” foreign-key relationships, selecting additional related-object data when it executes its query. This is a performance booster that results in a single, more complex query, but means later use of foreign-key relationships won’t require database queries.
Use for ForeignKey and OneToOne
It joins tables in a single query (SQL JOIN). Use when following single-valued relationships, i.e., ForeignKey and OneToOne fields.
Example:
```
Post.objects.select_related('author')
-> SELECT post.*, author.* FROM post JOIN author ON post.author_id = author.id
Post.objects.select_related('author', 'author__profile')
```
- `prefetch_related` - Returns a QuerySet that will automatically retrieve, in a single batch, related objects for each of the specified lookups. 
It does a separate lookup for each relationship and does the ‘joining’ in Python. Use when following multi-valued relationships, i.e., ManyToMany and Reverse ForeignKey.
Example:
```
Post.objects.prefetch_related('comment_set')[:10]
-> 
SELECT * FROM post LIMIT 10;
SELECT * FROM comment WHERE post_id IN (1,2,3,4,5,6,7,8,9,10);
```
Use `Prefetch` when you need control over the queryset being prefetched (filtering, ordering, selecting related fields, nested relationships, etc.):
```
from django.db.models import Prefetch

posts = Post.objects.prefetch_related(
    Prefetch('comments', queryset=Comment.objects.filter(active=True))
)
```
Both optimize query performance and solve the N+1 query problem when working with related models.
Combine both for complex queries:
```
Post.objects.select_related('category').prefetch_related('tags')
```
