[SCMFeature]
supported_scms%0 = P4
supported_scms%1 = Git
active_scm = 
engines#P4#server = 
engines#P4#user = 
engines#P4#password = 
engines#P4#start_server = False
engines#Git#server = 
engines#Git#repo_url = None
engines#Git#working_dir = .
engines#Git#user_name = 
engines#Git#password = 
poll_period = 36.0
number_history_items = 10
[SourceTreeFeature]
ignore_directories%0 = .git
ignore_directories%1 = .indigobuggie
ignore_suffixes%0 = swp
ignore_suffixes%1 = swn
ignore_suffixes%2 = pyc
ignore_suffixes%3 = o
root_directory = .
[TimeKeeperFeature]
use_repo = True
default_job = default
default_project = default
tracking = True
[MyTasksFeature]
auto_tasks = True
markers%0 = TODO
markers%1 = FIXME
markers%2 = TECH_DEBT
markers%3 = HACK
markers%4 = WTF
[CodeReviewFeature]
default = LocalCodeReviews
enabled_engines%0 = LocalCodeReviews
engines#LocalCodeReviews#root_directory = .
