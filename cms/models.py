from django.db import models

class MetaProject(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

class Project(models.Model):
    name = models.CharField(max_length=200)
    meta_project = models.ForeignKey(MetaProject, null=True, blank=True, on_delete=models.SET_NULL)
    description = models.TextField(null=True, blank=True)
    auto_generated = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Folder(models.Model):
    name = models.CharField(max_length=200)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)

    metadata_last_checked_at = models.DateTimeField(null=True, blank=True)
    last_file_change = models.DateTimeField(null=True, blank=True)
    still_exists = models.BooleanField(default=True)
    def __str__(self):
        return self.name

class Repository(models.Model):
    name = models.CharField(max_length=200)
    link = models.URLField(max_length=200)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)

    metadata_last_checked_at = models.DateTimeField(null=True, blank=True)
    stars = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    linked_website = models.URLField(max_length=200, null=True, blank=True)
    is_archived = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    nr_issues = models.IntegerField(null=True, blank=True)
    nr_open_issues = models.IntegerField(null=True, blank=True)
    last_commit_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

# set options for deployment_providers
class DeploymentProvider(models.TextChoices):
    HEROKU = 'heroku', 'Heroku'
    NETLIFY = 'netlify', 'Netlify'
    GITHUB_PAGES = 'github_pages', 'GitHub Pages'
    OTHER = 'other', 'Other'

class Deployment(models.Model):
    link = models.URLField(max_length=200)
    deployment_provider = models.CharField(max_length=200, choices=DeploymentProvider.choices)
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)
    should_track_pageviews = models.BooleanField(default=True)

    def __str__(self):
        return self.link

class GoatcounterTracker(models.Model):
    project = models.ForeignKey(Project, null=True, blank=True, on_delete=models.SET_NULL)
    goatcounter_id = models.CharField(max_length=200)
    api_key = models.CharField(max_length=200)

    def __str__(self):
        return self.goatcounter_id

class ContentType(models.TextChoices):
    TIKTOK = 'tiktok', 'TikTok'
    TWEET = 'tweet', 'Tweet'
    BLOG_POST = 'blog_post', 'Blog Post'
    REDDIT_POST = 'reddit_post', 'Reddit Post'
    REDDIT_ANSWER = 'reddit_answer', 'Reddit Answer'
    HN_POST = 'hn_post', 'Hacker News Post'
    HN_COMMENT = 'hn_comment', 'Hacker News Comment'
    OTHER = 'other', 'Other'


class PieceOfContent(models.Model):
    link = models.URLField(max_length=500, unique=True)
    content_type = models.CharField(max_length=200, choices=ContentType.choices)
    likes = models.IntegerField(null=True, blank=True)
    views = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    posted_at = models.DateTimeField(null=True, blank=True)

    @property
    def date(self):
        if self.posted_at:
            return self.posted_at
        else:
            return f'~ {self.created_at}'
    

class Settings(models.Model):
    local_projects_folder = models.CharField(max_length=200, null=True, blank=True)
    github_token = models.CharField(max_length=200, null=True, blank=True)
    tiktok_account_name = models.CharField(max_length=200, null=True, blank=True)
    tiktok_ms_token = models.CharField(max_length=400, null=True, blank=True)
    twitter_account_name = models.CharField(max_length=200, null=True, blank=True)
    twitter_bearer_token = models.CharField(max_length=400, null=True, blank=True)
    twitter_api_key = models.CharField(max_length=400, null=True, blank=True)
    twitter_api_secret = models.CharField(max_length=400, null=True, blank=True)
    twitter_access_token = models.CharField(max_length=400, null=True, blank=True)
    twitter_access_token_secret = models.CharField(max_length=400, null=True, blank=True)
    reddit_account_name = models.CharField(max_length=200, null=True, blank=True)
    hn_account_name = models.CharField(max_length=200, null=True, blank=True)
    
