| Bảng                                       | Cột                               | Kiểu dữ liệu                                         |
| ------------------------------------------ | --------------------------------- | ---------------------------------------------------- |
| auth_group                                 | id                                | int NOT NULL                                         |
| auth_group                                 | name                              | varchar(150) COLLATE utf8mb4_general_ci NOT NULL     |
| auth_group                                 | id                                | int NOT NULL                                         |
| auth_group                                 | group_id                          | int NOT NULL                                         |
| auth_group                                 | permission_id                     | int NOT NULL                                         |
| auth_group                                 | id                                | int NOT NULL                                         |
| auth_group                                 | name                              | varchar(255) COLLATE utf8mb4_general_ci NOT NULL     |
| auth_group                                 | content_type_id                   | int NOT NULL                                         |
| auth_group                                 | codename                          | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| auth_user_groups                           | id                                | int NOT NULL                                         |
| auth_user_groups                           | user_id                           | int NOT NULL                                         |
| auth_user_groups                           | group_id                          | int NOT NULL                                         |
| auth_user_groups                           | id                                | int NOT NULL                                         |
| auth_user_groups                           | user_id                           | int NOT NULL                                         |
| auth_user_groups                           | permission_id                     | int NOT NULL                                         |
| django_admin_log                           | id                                | int NOT NULL                                         |
| django_admin_log                           | action_time                       | datetime(6) NOT NULL                                 |
| django_admin_log                           | object_id                         | longtext COLLATE utf8mb4_general_ci                  |
| django_admin_log                           | object_repr                       | varchar(200) COLLATE utf8mb4_general_ci NOT NULL     |
| django_admin_log                           | action_flag                       | smallint UNSIGNED NOT NULL                           |
| django_admin_log                           | change_message                    | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| django_admin_log                           | content_type_id                   | int DEFAULT NULL                                     |
| django_admin_log                           | user_id                           | int NOT NULL                                         |
| django_content_type                        | id                                | int NOT NULL                                         |
| django_content_type                        | app_label                         | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| django_content_type                        | model                             | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| django_flatpage                            | id                                | int NOT NULL                                         |
| django_flatpage                            | url                               | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| django_flatpage                            | title                             | varchar(200) COLLATE utf8mb4_general_ci NOT NULL     |
| django_flatpage                            | content                           | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| django_flatpage                            | enable_comments                   | tinyint(1) NOT NULL                                  |
| django_flatpage                            | template_name                     | varchar(70) COLLATE utf8mb4_general_ci NOT NULL      |
| django_flatpage                            | registration_required             | tinyint(1) NOT NULL                                  |
| django_flatpage_sites                      | id                                | int NOT NULL                                         |
| django_flatpage_sites                      | flatpage_id                       | int NOT NULL                                         |
| django_flatpage_sites                      | site_id                           | int NOT NULL                                         |
| django_migrations                          | id                                | int NOT NULL                                         |
| django_migrations                          | app                               | varchar(255) COLLATE utf8mb4_general_ci NOT NULL     |
| django_migrations                          | name                              | varchar(255) COLLATE utf8mb4_general_ci NOT NULL     |
| django_migrations                          | applied                           | datetime(6) NOT NULL                                 |
| django_redirect                            | id                                | int NOT NULL                                         |
| django_redirect                            | site_id                           | int NOT NULL                                         |
| django_redirect                            | old_path                          | varchar(200) COLLATE utf8mb4_general_ci NOT NULL     |
| django_redirect                            | new_path                          | varchar(200) COLLATE utf8mb4_general_ci NOT NULL     |
| django_redirect                            | session_key                       | varchar(40) COLLATE utf8mb4_general_ci NOT NULL      |
| django_redirect                            | session_data                      | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| django_redirect                            | expire_date                       | datetime(6) NOT NULL                                 |
| django_site                                | id                                | int NOT NULL                                         |
| django_site                                | domain                            | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| django_site                                | name                              | varchar(50) COLLATE utf8mb4_general_ci NOT NULL      |
| impersonate_impersonationlog               | id                                | int NOT NULL                                         |
| impersonate_impersonationlog               | session_key                       | varchar(40) COLLATE utf8mb4_general_ci NOT NULL      |
| impersonate_impersonationlog               | session_started_at                | datetime(6) DEFAULT NULL                             |
| impersonate_impersonationlog               | session_ended_at                  | datetime(6) DEFAULT NULL                             |
| impersonate_impersonationlog               | impersonating_id                  | int NOT NULL                                         |
| impersonate_impersonationlog               | impersonator_id                   | int NOT NULL                                         |
| judge_badge                                | id                                | int NOT NULL                                         |
| judge_badge                                | name                              | varchar(128) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_badge                                | mini                              | varchar(200) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_badge                                | full_size                         | varchar(200) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_badge                                | id                                | int NOT NULL                                         |
| judge_badge                                | title                             | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_badge                                | slug                              | varchar(50) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_badge                                | visible                           | tinyint(1) NOT NULL                                  |
| judge_badge                                | sticky                            | tinyint(1) NOT NULL                                  |
| judge_badge                                | publish_on                        | datetime(6) NOT NULL                                 |
| judge_badge                                | content                           | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_badge                                | summary                           | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_badge                                | og_image                          | varchar(150) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_badge                                | global_post                       | tinyint(1) NOT NULL                                  |
| judge_badge                                | organization_id                   | int DEFAULT NULL                                     |
| judge_badge                                | score                             | int NOT NULL                                         |
| judge_blogpost_authors                     | id                                | int NOT NULL                                         |
| judge_blogpost_authors                     | blogpost_id                       | int NOT NULL                                         |
| judge_blogpost_authors                     | profile_id                        | int NOT NULL                                         |
| judge_blogvote                             | id                                | int NOT NULL                                         |
| judge_blogvote                             | score                             | int NOT NULL                                         |
| judge_blogvote                             | blog_id                           | int NOT NULL                                         |
| judge_blogvote                             | voter_id                          | int NOT NULL                                         |
| judge_blogvote                             | id                                | int NOT NULL                                         |
| judge_blogvote                             | time                              | datetime(6) NOT NULL                                 |
| judge_blogvote                             | page                              | varchar(34) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_blogvote                             | score                             | int NOT NULL                                         |
| judge_blogvote                             | body                              | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_blogvote                             | hidden                            | tinyint(1) NOT NULL                                  |
| judge_blogvote                             | lft                               | int UNSIGNED NOT NULL                                |
| judge_blogvote                             | rght                              | int UNSIGNED NOT NULL                                |
| judge_blogvote                             | tree_id                           | int UNSIGNED NOT NULL                                |
| judge_blogvote                             | level                             | int UNSIGNED NOT NULL                                |
| judge_blogvote                             | author_id                         | int NOT NULL                                         |
| judge_blogvote                             | parent_id                         | int DEFAULT NULL                                     |
| judge_blogvote                             | revisions                         | int NOT NULL                                         |
| judge_commentlock                          | id                                | int NOT NULL                                         |
| judge_commentlock                          | page                              | varchar(34) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_commentlock                          | id                                | int NOT NULL                                         |
| judge_commentlock                          | score                             | int NOT NULL                                         |
| judge_commentlock                          | comment_id                        | int NOT NULL                                         |
| judge_commentlock                          | voter_id                          | int NOT NULL                                         |
| judge_commentlock                          | id                                | int NOT NULL                                         |
| judge_commentlock                          | key                               | varchar(32) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_commentlock                          | name                              | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_commentlock                          | description                       | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_commentlock                          | start_time                        | datetime(6) NOT NULL                                 |
| judge_commentlock                          | end_time                          | datetime(6) NOT NULL                                 |
| judge_commentlock                          | time_limit                        | bigint DEFAULT NULL                                  |
| judge_commentlock                          | is_visible                        | tinyint(1) NOT NULL                                  |
| judge_commentlock                          | is_rated                          | tinyint(1) NOT NULL                                  |
| judge_commentlock                          | use_clarifications                | tinyint(1) NOT NULL                                  |
| judge_commentlock                          | rate_all                          | tinyint(1) NOT NULL                                  |
| judge_commentlock                          | is_private                        | tinyint(1) NOT NULL                                  |
| judge_commentlock                          | hide_problem_tags                 | tinyint(1) NOT NULL                                  |
| judge_commentlock                          | run_pretests_only                 | tinyint(1) NOT NULL                                  |
| judge_commentlock                          | og_image                          | varchar(150) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_commentlock                          | logo_override_image               | varchar(150) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_commentlock                          | user_count                        | int NOT NULL                                         |
| judge_commentlock                          | summary                           | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_commentlock                          | access_code                       | varchar(255) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_commentlock                          | format_name                       | varchar(32) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_commentlock                          | format_config                     | longtext COLLATE utf8mb4_general_ci                  |
| judge_commentlock                          | rating_ceiling                    | int DEFAULT NULL                                     |
| judge_commentlock                          | rating_floor                      | int DEFAULT NULL                                     |
| judge_commentlock                          | is_organization_private           | tinyint(1) NOT NULL                                  |
| judge_commentlock                          | problem_label_script              | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_commentlock                          | points_precision                  | int NOT NULL                                         |
| judge_commentlock                          | scoreboard_visibility             | varchar(1) COLLATE utf8mb4_general_ci NOT NULL       |
| judge_commentlock                          | virtual_count                     | int NOT NULL                                         |
| judge_commentlock                          | locked_after                      | datetime(6) DEFAULT NULL                             |
| judge_commentlock                          | hide_problem_authors              | tinyint(1) NOT NULL                                  |
| judge_commentlock                          | csv_ranking                       | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_commentlock                          | show_short_display                | tinyint(1) NOT NULL                                  |
| judge_commentlock                          | push_announcements                | tinyint(1) NOT NULL                                  |
| judge_commentlock                          | frozen_last_minutes               | int NOT NULL                                         |
| judge_commentlock                          | show_submission_list              | tinyint(1) NOT NULL                                  |
| judge_commentlock                          | scoreboard_cache_timeout          | int UNSIGNED NOT NULL                                |
| judge_commentlock                          | data_last_downloaded              | datetime(6) DEFAULT NULL                             |
| judge_commentlock                          | disallow_virtual                  | tinyint(1) NOT NULL                                  |
| judge_commentlock                          | ranking_access_code               | varchar(255) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_commentlock                          | registration_end                  | datetime(6) DEFAULT NULL                             |
| judge_commentlock                          | registration_start                | datetime(6) DEFAULT NULL                             |
| judge_contestannouncement                  | id                                | int NOT NULL                                         |
| judge_contestannouncement                  | title                             | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_contestannouncement                  | description                       | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_contestannouncement                  | date                              | datetime(6) NOT NULL                                 |
| judge_contestannouncement                  | contest_id                        | int NOT NULL                                         |
| judge_contestannouncement                  | id                                | int NOT NULL                                         |
| judge_contestannouncement                  | language                          | varchar(10) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_contestannouncement                  | submission_count                  | int UNSIGNED NOT NULL                                |
| judge_contestannouncement                  | url                               | varchar(200) COLLATE utf8mb4_general_ci DEFAULT NULL |
| judge_contestannouncement                  | contest_id                        | int NOT NULL                                         |
| judge_contestannouncement                  | problem_id                        | int NOT NULL                                         |
| judge_contestparticipation                 | id                                | int NOT NULL                                         |
| judge_contestparticipation                 | start                             | datetime(6) NOT NULL                                 |
| judge_contestparticipation                 | score                             | double NOT NULL                                      |
| judge_contestparticipation                 | cumtime                           | int UNSIGNED NOT NULL                                |
| judge_contestparticipation                 | virtual                           | int NOT NULL                                         |
| judge_contestparticipation                 | format_data                       | longtext COLLATE utf8mb4_general_ci                  |
| judge_contestparticipation                 | contest_id                        | int NOT NULL                                         |
| judge_contestparticipation                 | user_id                           | int NOT NULL                                         |
| judge_contestparticipation                 | is_disqualified                   | tinyint(1) NOT NULL                                  |
| judge_contestparticipation                 | tiebreaker                        | double NOT NULL                                      |
| judge_contestparticipation                 | frozen_cumtime                    | int UNSIGNED NOT NULL                                |
| judge_contestparticipation                 | frozen_score                      | double NOT NULL                                      |
| judge_contestparticipation                 | frozen_tiebreaker                 | double NOT NULL                                      |
| judge_contestproblem                       | id                                | int NOT NULL                                         |
| judge_contestproblem                       | points                            | int NOT NULL                                         |
| judge_contestproblem                       | partial                           | tinyint(1) NOT NULL                                  |
| judge_contestproblem                       | is_pretested                      | tinyint(1) NOT NULL                                  |
| judge_contestproblem                       | order                             | int UNSIGNED NOT NULL                                |
| judge_contestproblem                       | output_prefix_override            | int DEFAULT NULL                                     |
| judge_contestproblem                       | max_submissions                   | int DEFAULT NULL                                     |
| judge_contestproblem                       | contest_id                        | int NOT NULL                                         |
| judge_contestproblem                       | problem_id                        | int NOT NULL                                         |
| judge_contestsubmission                    | id                                | int NOT NULL                                         |
| judge_contestsubmission                    | points                            | double NOT NULL                                      |
| judge_contestsubmission                    | is_pretest                        | tinyint(1) NOT NULL                                  |
| judge_contestsubmission                    | participation_id                  | int NOT NULL                                         |
| judge_contestsubmission                    | problem_id                        | int NOT NULL                                         |
| judge_contestsubmission                    | submission_id                     | int NOT NULL                                         |
| judge_contesttag                           | id                                | int NOT NULL                                         |
| judge_contesttag                           | name                              | varchar(20) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_contesttag                           | color                             | varchar(7) COLLATE utf8mb4_general_ci NOT NULL       |
| judge_contesttag                           | description                       | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_contesttag                           | id                                | int NOT NULL                                         |
| judge_contesttag                           | contest_id                        | int NOT NULL                                         |
| judge_contesttag                           | profile_id                        | int NOT NULL                                         |
| judge_contest_banned_judges                | id                                | int NOT NULL                                         |
| judge_contest_banned_judges                | contest_id                        | int NOT NULL                                         |
| judge_contest_banned_judges                | judge_id                          | int NOT NULL                                         |
| judge_contest_banned_judges                | id                                | int NOT NULL                                         |
| judge_contest_banned_judges                | contest_id                        | int NOT NULL                                         |
| judge_contest_banned_judges                | profile_id                        | int NOT NULL                                         |
| judge_contest_banned_judges                | id                                | int NOT NULL                                         |
| judge_contest_banned_judges                | contest_id                        | int NOT NULL                                         |
| judge_contest_banned_judges                | profile_id                        | int NOT NULL                                         |
| judge_contest_banned_judges                | id                                | int NOT NULL                                         |
| judge_contest_banned_judges                | contest_id                        | int NOT NULL                                         |
| judge_contest_banned_judges                | organization_id                   | int NOT NULL                                         |
| judge_contest_private_contestants          | id                                | int NOT NULL                                         |
| judge_contest_private_contestants          | contest_id                        | int NOT NULL                                         |
| judge_contest_private_contestants          | profile_id                        | int NOT NULL                                         |
| judge_contest_rate_exclude                 | id                                | int NOT NULL                                         |
| judge_contest_rate_exclude                 | contest_id                        | int NOT NULL                                         |
| judge_contest_rate_exclude                 | profile_id                        | int NOT NULL                                         |
| judge_contest_rate_exclude                 | id                                | int NOT NULL                                         |
| judge_contest_rate_exclude                 | contest_id                        | int NOT NULL                                         |
| judge_contest_rate_exclude                 | contesttag_id                     | int NOT NULL                                         |
| judge_contest_rate_exclude                 | id                                | int NOT NULL                                         |
| judge_contest_rate_exclude                 | contest_id                        | int NOT NULL                                         |
| judge_contest_rate_exclude                 | profile_id                        | int NOT NULL                                         |
| judge_contest_view_contest_scoreboard      | id                                | int NOT NULL                                         |
| judge_contest_view_contest_scoreboard      | contest_id                        | int NOT NULL                                         |
| judge_contest_view_contest_scoreboard      | profile_id                        | int NOT NULL                                         |
| judge_generalissue                         | id                                | int NOT NULL                                         |
| judge_generalissue                         | issue_url                         | varchar(200) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_generalissue                         | id                                | int NOT NULL                                         |
| judge_generalissue                         | name                              | varchar(50) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_generalissue                         | created                           | datetime(6) NOT NULL                                 |
| judge_generalissue                         | auth_key                          | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_generalissue                         | is_blocked                        | tinyint(1) NOT NULL                                  |
| judge_generalissue                         | online                            | tinyint(1) NOT NULL                                  |
| judge_generalissue                         | start_time                        | datetime(6) DEFAULT NULL                             |
| judge_generalissue                         | ping                              | double DEFAULT NULL                                  |
| judge_generalissue                         | load                              | double DEFAULT NULL                                  |
| judge_generalissue                         | description                       | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_generalissue                         | last_ip                           | char(39) COLLATE utf8mb4_general_ci DEFAULT NULL     |
| judge_generalissue                         | is_disabled                       | tinyint(1) NOT NULL                                  |
| judge_generalissue                         | tier                              | int UNSIGNED NOT NULL                                |
| judge_judge_problems                       | id                                | int NOT NULL                                         |
| judge_judge_problems                       | judge_id                          | int NOT NULL                                         |
| judge_judge_problems                       | problem_id                        | int NOT NULL                                         |
| judge_judge_runtimes                       | id                                | int NOT NULL                                         |
| judge_judge_runtimes                       | judge_id                          | int NOT NULL                                         |
| judge_judge_runtimes                       | language_id                       | int NOT NULL                                         |
| judge_language                             | id                                | int NOT NULL                                         |
| judge_language                             | key                               | varchar(10) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_language                             | name                              | varchar(20) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_language                             | short_name                        | varchar(10) COLLATE utf8mb4_general_ci DEFAULT NULL  |
| judge_language                             | common_name                       | varchar(20) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_language                             | ace                               | varchar(20) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_language                             | pygments                          | varchar(20) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_language                             | template                          | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_language                             | info                              | varchar(50) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_language                             | description                       | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_language                             | extension                         | varchar(10) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_language                             | file_only                         | tinyint(1) NOT NULL                                  |
| judge_language                             | file_size_limit                   | int NOT NULL                                         |
| judge_language                             | include_in_problem                | tinyint(1) NOT NULL                                  |
| judge_languagelimit                        | id                                | int NOT NULL                                         |
| judge_languagelimit                        | time_limit                        | double NOT NULL                                      |
| judge_languagelimit                        | memory_limit                      | int NOT NULL                                         |
| judge_languagelimit                        | language_id                       | int NOT NULL                                         |
| judge_languagelimit                        | problem_id                        | int NOT NULL                                         |
| judge_languagelimit                        | id                                | int NOT NULL                                         |
| judge_languagelimit                        | key                               | varchar(20) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_languagelimit                        | link                              | varchar(256) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_languagelimit                        | name                              | varchar(256) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_languagelimit                        | display                           | varchar(256) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_languagelimit                        | icon                              | varchar(256) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_languagelimit                        | text                              | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_languagelimit                        | id                                | int NOT NULL                                         |
| judge_languagelimit                        | key                               | varchar(30) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_languagelimit                        | value                             | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_languagelimit                        | id                                | int NOT NULL                                         |
| judge_languagelimit                        | order                             | int UNSIGNED NOT NULL                                |
| judge_languagelimit                        | key                               | varchar(10) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_languagelimit                        | label                             | varchar(20) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_languagelimit                        | path                              | varchar(255) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_languagelimit                        | regex                             | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_languagelimit                        | lft                               | int UNSIGNED NOT NULL                                |
| judge_languagelimit                        | rght                              | int UNSIGNED NOT NULL                                |
| judge_languagelimit                        | tree_id                           | int UNSIGNED NOT NULL                                |
| judge_languagelimit                        | level                             | int UNSIGNED NOT NULL                                |
| judge_languagelimit                        | parent_id                         | int DEFAULT NULL                                     |
| judge_organization                         | id                                | int NOT NULL                                         |
| judge_organization                         | name                              | varchar(128) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_organization                         | slug                              | varchar(128) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_organization                         | short_name                        | varchar(20) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_organization                         | about                             | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_organization                         | creation_date                     | datetime(6) NOT NULL                                 |
| judge_organization                         | is_open                           | tinyint(1) NOT NULL                                  |
| judge_organization                         | slots                             | int DEFAULT NULL                                     |
| judge_organization                         | access_code                       | varchar(7) COLLATE utf8mb4_general_ci DEFAULT NULL   |
| judge_organization                         | logo_override_image               | varchar(150) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_organization                         | performance_points                | double NOT NULL                                      |
| judge_organization                         | member_count                      | int NOT NULL                                         |
| judge_organization                         | is_unlisted                       | tinyint(1) NOT NULL                                  |
| judge_organization                         | available_credit                  | double NOT NULL                                      |
| judge_organization                         | current_consumed_credit           | double NOT NULL                                      |
| judge_organization                         | monthly_credit                    | double NOT NULL                                      |
| judge_organizationmonthlyusage             | id                                | int NOT NULL                                         |
| judge_organizationmonthlyusage             | time                              | date NOT NULL                                        |
| judge_organizationmonthlyusage             | consumed_credit                   | double NOT NULL                                      |
| judge_organizationmonthlyusage             | organization_id                   | int NOT NULL                                         |
| judge_organizationmonthlyusage             | id                                | int NOT NULL                                         |
| judge_organizationmonthlyusage             | time                              | datetime(6) NOT NULL                                 |
| judge_organizationmonthlyusage             | state                             | varchar(1) COLLATE utf8mb4_general_ci NOT NULL       |
| judge_organizationmonthlyusage             | reason                            | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_organizationmonthlyusage             | organization_id                   | int NOT NULL                                         |
| judge_organizationmonthlyusage             | user_id                           | int NOT NULL                                         |
| judge_organizationmonthlyusage             | id                                | int NOT NULL                                         |
| judge_organizationmonthlyusage             | organization_id                   | int NOT NULL                                         |
| judge_organizationmonthlyusage             | profile_id                        | int NOT NULL                                         |
| judge_problem                              | id                                | int NOT NULL                                         |
| judge_problem                              | code                              | varchar(32) NOT NULL                                 |
| judge_problem                              | name                              | varchar(100) NOT NULL                                |
| judge_problem                              | description                       | longtext NOT NULL                                    |
| judge_problem                              | time_limit                        | double NOT NULL                                      |
| judge_problem                              | memory_limit                      | int UNSIGNED NOT NULL                                |
| judge_problem                              | short_circuit                     | tinyint(1) NOT NULL                                  |
| judge_problem                              | points                            | double NOT NULL                                      |
| judge_problem                              | partial                           | tinyint(1) NOT NULL                                  |
| judge_problem                              | is_public                         | tinyint(1) NOT NULL                                  |
| judge_problem                              | is_manually_managed               | tinyint(1) NOT NULL                                  |
| judge_problem                              | date                              | datetime(6) DEFAULT NULL                             |
| judge_problem                              | og_image                          | varchar(150) NOT NULL                                |
| judge_problem                              | summary                           | longtext NOT NULL                                    |
| judge_problem                              | user_count                        | int NOT NULL                                         |
| judge_problem                              | ac_rate                           | double NOT NULL                                      |
| judge_problem                              | is_organization_private           | tinyint(1) NOT NULL                                  |
| judge_problem                              | group_id                          | int NOT NULL                                         |
| judge_problem                              | license_id                        | int DEFAULT NULL                                     |
| judge_problem                              | is_full_markup                    | tinyint(1) NOT NULL                                  |
| judge_problem                              | pdf_url                           | varchar(200) NOT NULL                                |
| judge_problem                              | source                            | varchar(200) NOT NULL                                |
| judge_problem                              | suggester_id                      | int DEFAULT NULL                                     |
| judge_problem                              | submission_source_visibility_mode | varchar(1) NOT NULL                                  |
| judge_problem                              | testcase_visibility_mode          | varchar(1) NOT NULL                                  |
| judge_problem                              | allow_view_feedback               | tinyint(1) NOT NULL                                  |
| judge_problem                              | testcase_result_visibility_mode   | varchar(1) NOT NULL                                  |
| judge_problemclarification                 | id                                | int NOT NULL                                         |
| judge_problemclarification                 | description                       | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_problemclarification                 | date                              | datetime(6) NOT NULL                                 |
| judge_problemclarification                 | problem_id                        | int NOT NULL                                         |
| judge_problemclarification                 | id                                | int NOT NULL                                         |
| judge_problemclarification                 | zipfile                           | varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL |
| judge_problemclarification                 | generator                         | varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL |
| judge_problemclarification                 | output_prefix                     | int DEFAULT NULL                                     |
| judge_problemclarification                 | output_limit                      | int DEFAULT NULL                                     |
| judge_problemclarification                 | feedback                          | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_problemclarification                 | checker                           | varchar(10) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_problemclarification                 | checker_args                      | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_problemclarification                 | problem_id                        | int NOT NULL                                         |
| judge_problemclarification                 | custom_checker                    | varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL |
| judge_problemclarification                 | custom_grader                     | varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL |
| judge_problemclarification                 | custom_header                     | varchar(100) COLLATE utf8mb4_general_ci DEFAULT NULL |
| judge_problemclarification                 | grader                            | varchar(30) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_problemclarification                 | grader_args                       | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_problemclarification                 | nobigmath                         | tinyint(1) DEFAULT NULL                              |
| judge_problemclarification                 | unicode                           | tinyint(1) DEFAULT NULL                              |
| judge_problemgroup                         | id                                | int NOT NULL                                         |
| judge_problemgroup                         | name                              | varchar(20) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_problemgroup                         | full_name                         | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_problemtestcase                      | id                                | int NOT NULL                                         |
| judge_problemtestcase                      | order                             | int NOT NULL                                         |
| judge_problemtestcase                      | type                              | varchar(1) COLLATE utf8mb4_general_ci NOT NULL       |
| judge_problemtestcase                      | input_file                        | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_problemtestcase                      | output_file                       | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_problemtestcase                      | generator_args                    | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_problemtestcase                      | points                            | int DEFAULT NULL                                     |
| judge_problemtestcase                      | is_pretest                        | tinyint(1) NOT NULL                                  |
| judge_problemtestcase                      | output_prefix                     | int DEFAULT NULL                                     |
| judge_problemtestcase                      | output_limit                      | int DEFAULT NULL                                     |
| judge_problemtestcase                      | checker                           | varchar(10) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_problemtestcase                      | checker_args                      | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_problemtestcase                      | dataset_id                        | int NOT NULL                                         |
| judge_problemtranslation                   | id                                | int NOT NULL                                         |
| judge_problemtranslation                   | language                          | varchar(7) COLLATE utf8mb4_general_ci NOT NULL       |
| judge_problemtranslation                   | name                              | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_problemtranslation                   | description                       | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_problemtranslation                   | problem_id                        | int NOT NULL                                         |
| judge_problemtranslation                   | id                                | int NOT NULL                                         |
| judge_problemtranslation                   | name                              | varchar(20) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_problemtranslation                   | full_name                         | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_problem_allowed_languages            | id                                | int NOT NULL                                         |
| judge_problem_allowed_languages            | problem_id                        | int NOT NULL                                         |
| judge_problem_allowed_languages            | language_id                       | int NOT NULL                                         |
| judge_problem_authors                      | id                                | int NOT NULL                                         |
| judge_problem_authors                      | problem_id                        | int NOT NULL                                         |
| judge_problem_authors                      | profile_id                        | int NOT NULL                                         |
| judge_problem_banned_users                 | id                                | int NOT NULL                                         |
| judge_problem_banned_users                 | problem_id                        | int NOT NULL                                         |
| judge_problem_banned_users                 | profile_id                        | int NOT NULL                                         |
| judge_problem_banned_users                 | id                                | int NOT NULL                                         |
| judge_problem_banned_users                 | problem_id                        | int NOT NULL                                         |
| judge_problem_banned_users                 | profile_id                        | int NOT NULL                                         |
| judge_problem_organizations                | id                                | int NOT NULL                                         |
| judge_problem_organizations                | problem_id                        | int NOT NULL                                         |
| judge_problem_organizations                | organization_id                   | int NOT NULL                                         |
| judge_problem_testers                      | id                                | int NOT NULL                                         |
| judge_problem_testers                      | problem_id                        | int NOT NULL                                         |
| judge_problem_testers                      | profile_id                        | int NOT NULL                                         |
| judge_problem_testers                      | id                                | int NOT NULL                                         |
| judge_problem_testers                      | problem_id                        | int NOT NULL                                         |
| judge_problem_testers                      | problemtype_id                    | int NOT NULL                                         |
| judge_profile                              | id                                | int NOT NULL                                         |
| judge_profile                              | about                             | longtext COLLATE utf8mb4_general_ci                  |
| judge_profile                              | timezone                          | varchar(50) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_profile                              | points                            | double NOT NULL                                      |
| judge_profile                              | performance_points                | double NOT NULL                                      |
| judge_profile                              | problem_count                     | int NOT NULL                                         |
| judge_profile                              | ace_theme                         | varchar(30) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_profile                              | last_access                       | datetime(6) NOT NULL                                 |
| judge_profile                              | ip                                | char(39) COLLATE utf8mb4_general_ci DEFAULT NULL     |
| judge_profile                              | display_rank                      | varchar(10) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_profile                              | mute                              | tinyint(1) NOT NULL                                  |
| judge_profile                              | is_unlisted                       | tinyint(1) NOT NULL                                  |
| judge_profile                              | rating                            | int DEFAULT NULL                                     |
| judge_profile                              | user_script                       | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_profile                              | math_engine                       | varchar(4) COLLATE utf8mb4_general_ci NOT NULL       |
| judge_profile                              | is_totp_enabled                   | tinyint(1) NOT NULL                                  |
| judge_profile                              | totp_key                          | longblob                                             |
| judge_profile                              | notes                             | longtext COLLATE utf8mb4_general_ci                  |
| judge_profile                              | current_contest_id                | int DEFAULT NULL                                     |
| judge_profile                              | language_id                       | int NOT NULL                                         |
| judge_profile                              | user_id                           | int NOT NULL                                         |
| judge_profile                              | api_token                         | varchar(64) COLLATE utf8mb4_general_ci DEFAULT NULL  |
| judge_profile                              | is_webauthn_enabled               | tinyint(1) NOT NULL                                  |
| judge_profile                              | data_last_downloaded              | datetime(6) DEFAULT NULL                             |
| judge_profile                              | scratch_codes                     | longblob                                             |
| judge_profile                              | contribution_points               | int NOT NULL                                         |
| judge_profile                              | allow_tagging                     | tinyint(1) NOT NULL                                  |
| judge_profile                              | last_totp_timecode                | int NOT NULL                                         |
| judge_profile                              | ban_reason                        | longtext COLLATE utf8mb4_general_ci                  |
| judge_profile                              | username_display_override         | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_profile                              | display_badge_id                  | int DEFAULT NULL                                     |
| judge_profile                              | site_theme                        | varchar(10) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_profile                              | vnoj_points                       | int NOT NULL                                         |
| judge_profile                              | ip_auth                           | char(39) COLLATE utf8mb4_general_ci DEFAULT NULL     |
| judge_profile_badges                       | id                                | int NOT NULL                                         |
| judge_profile_badges                       | profile_id                        | int NOT NULL                                         |
| judge_profile_badges                       | badge_id                          | int NOT NULL                                         |
| judge_profile_badges                       | id                                | int NOT NULL                                         |
| judge_profile_badges                       | sort_value                        | int NOT NULL                                         |
| judge_profile_badges                       | profile_id                        | int NOT NULL                                         |
| judge_profile_badges                       | organization_id                   | int NOT NULL                                         |
| judge_rating                               | id                                | int NOT NULL                                         |
| judge_rating                               | rank                              | int NOT NULL                                         |
| judge_rating                               | rating                            | int NOT NULL                                         |
| judge_rating                               | last_rated                        | datetime(6) NOT NULL                                 |
| judge_rating                               | contest_id                        | int NOT NULL                                         |
| judge_rating                               | participation_id                  | int NOT NULL                                         |
| judge_rating                               | user_id                           | int NOT NULL                                         |
| judge_rating                               | mean                              | double NOT NULL                                      |
| judge_rating                               | performance                       | double NOT NULL                                      |
| judge_rating                               | id                                | int NOT NULL                                         |
| judge_rating                               | name                              | varchar(64) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_rating                               | version                           | varchar(64) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_rating                               | priority                          | int NOT NULL                                         |
| judge_rating                               | judge_id                          | int NOT NULL                                         |
| judge_rating                               | language_id                       | int NOT NULL                                         |
| judge_solution                             | id                                | int NOT NULL                                         |
| judge_solution                             | is_public                         | tinyint(1) NOT NULL                                  |
| judge_solution                             | publish_on                        | datetime(6) NOT NULL                                 |
| judge_solution                             | content                           | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_solution                             | problem_id                        | int NOT NULL                                         |
| judge_solution_authors                     | id                                | int NOT NULL                                         |
| judge_solution_authors                     | solution_id                       | int NOT NULL                                         |
| judge_solution_authors                     | profile_id                        | int NOT NULL                                         |
| judge_submission                           | id                                | int NOT NULL                                         |
| judge_submission                           | date                              | datetime(6) NOT NULL                                 |
| judge_submission                           | time                              | double DEFAULT NULL                                  |
| judge_submission                           | memory                            | double DEFAULT NULL                                  |
| judge_submission                           | points                            | double DEFAULT NULL                                  |
| judge_submission                           | status                            | varchar(2) COLLATE utf8mb4_general_ci NOT NULL       |
| judge_submission                           | result                            | varchar(3) COLLATE utf8mb4_general_ci DEFAULT NULL   |
| judge_submission                           | error                             | longtext COLLATE utf8mb4_general_ci                  |
| judge_submission                           | current_testcase                  | int NOT NULL                                         |
| judge_submission                           | batch                             | tinyint(1) NOT NULL                                  |
| judge_submission                           | case_points                       | double NOT NULL                                      |
| judge_submission                           | case_total                        | double NOT NULL                                      |
| judge_submission                           | is_pretested                      | tinyint(1) NOT NULL                                  |
| judge_submission                           | judged_on_id                      | int DEFAULT NULL                                     |
| judge_submission                           | language_id                       | int NOT NULL                                         |
| judge_submission                           | problem_id                        | int NOT NULL                                         |
| judge_submission                           | user_id                           | int NOT NULL                                         |
| judge_submission                           | contest_object_id                 | int DEFAULT NULL                                     |
| judge_submission                           | judged_date                       | datetime(6) DEFAULT NULL                             |
| judge_submission                           | locked_after                      | datetime(6) DEFAULT NULL                             |
| judge_submission                           | rejudged_date                     | datetime(6) DEFAULT NULL                             |
| judge_submissionsource                     | id                                | int NOT NULL                                         |
| judge_submissionsource                     | source                            | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_submissionsource                     | submission_id                     | int NOT NULL                                         |
| judge_submissiontestcase                   | id                                | int NOT NULL                                         |
| judge_submissiontestcase                   | case                              | int NOT NULL                                         |
| judge_submissiontestcase                   | status                            | varchar(3) COLLATE utf8mb4_general_ci NOT NULL       |
| judge_submissiontestcase                   | time                              | double DEFAULT NULL                                  |
| judge_submissiontestcase                   | memory                            | double DEFAULT NULL                                  |
| judge_submissiontestcase                   | points                            | double DEFAULT NULL                                  |
| judge_submissiontestcase                   | total                             | double DEFAULT NULL                                  |
| judge_submissiontestcase                   | batch                             | int DEFAULT NULL                                     |
| judge_submissiontestcase                   | feedback                          | varchar(50) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_submissiontestcase                   | extended_feedback                 | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_submissiontestcase                   | output                            | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_submissiontestcase                   | submission_id                     | int NOT NULL                                         |
| judge_tag                                  | id                                | int NOT NULL                                         |
| judge_tag                                  | code                              | varchar(30) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_tag                                  | name                              | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_tag                                  | group_id                          | int NOT NULL                                         |
| judge_tag                                  | id                                | int NOT NULL                                         |
| judge_tag                                  | assigner_id                       | int NOT NULL                                         |
| judge_tag                                  | problem_id                        | int NOT NULL                                         |
| judge_tag                                  | tag_id                            | int NOT NULL                                         |
| judge_tag                                  | id                                | int NOT NULL                                         |
| judge_tag                                  | code                              | varchar(30) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_tag                                  | name                              | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_tag                                  | id                                | int NOT NULL                                         |
| judge_tag                                  | code                              | varchar(32) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_tag                                  | name                              | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_tag                                  | link                              | varchar(200) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_tag                                  | judge                             | varchar(30) COLLATE utf8mb4_general_ci DEFAULT NULL  |
| judge_tag                                  | id                                | int NOT NULL                                         |
| judge_tag                                  | title                             | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_tag                                  | time                              | datetime(6) NOT NULL                                 |
| judge_tag                                  | notes                             | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_tag                                  | object_id                         | int UNSIGNED NOT NULL                                |
| judge_tag                                  | is_open                           | tinyint(1) NOT NULL                                  |
| judge_tag                                  | content_type_id                   | int NOT NULL                                         |
| judge_tag                                  | user_id                           | int NOT NULL                                         |
| judge_tag                                  | is_contributive                   | tinyint(1) NOT NULL                                  |
| judge_ticketmessage                        | id                                | int NOT NULL                                         |
| judge_ticketmessage                        | body                              | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_ticketmessage                        | time                              | datetime(6) NOT NULL                                 |
| judge_ticketmessage                        | ticket_id                         | int NOT NULL                                         |
| judge_ticketmessage                        | user_id                           | int NOT NULL                                         |
| judge_ticket_assignees                     | id                                | int NOT NULL                                         |
| judge_ticket_assignees                     | ticket_id                         | int NOT NULL                                         |
| judge_ticket_assignees                     | profile_id                        | int NOT NULL                                         |
| judge_webauthncredential                   | id                                | int NOT NULL                                         |
| judge_webauthncredential                   | name                              | varchar(100) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_webauthncredential                   | cred_id                           | varchar(255) COLLATE utf8mb4_general_ci NOT NULL     |
| judge_webauthncredential                   | public_key                        | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| judge_webauthncredential                   | counter                           | bigint NOT NULL                                      |
| judge_webauthncredential                   | user_id                           | int NOT NULL                                         |
| judge_webauthncredential                   | id                                | int NOT NULL                                         |
| judge_webauthncredential                   | activation_key                    | varchar(64) COLLATE utf8mb4_general_ci NOT NULL      |
| judge_webauthncredential                   | user_id                           | int NOT NULL                                         |
| judge_webauthncredential                   | activated                         | tinyint(1) NOT NULL                                  |
| registration_supervisedregistrationprofile | registrationprofile_ptr_id        | int NOT NULL                                         |
| registration_supervisedregistrationprofile | id                                | int NOT NULL                                         |
| registration_supervisedregistrationprofile | date_created                      | datetime(6) NOT NULL                                 |
| registration_supervisedregistrationprofile | comment                           | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| registration_supervisedregistrationprofile | user_id                           | int DEFAULT NULL                                     |
| reversion_version                          | id                                | int NOT NULL                                         |
| reversion_version                          | object_id                         | varchar(191) COLLATE utf8mb4_general_ci NOT NULL     |
| reversion_version                          | format                            | varchar(255) COLLATE utf8mb4_general_ci NOT NULL     |
| reversion_version                          | serialized_data                   | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| reversion_version                          | object_repr                       | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| reversion_version                          | content_type_id                   | int NOT NULL                                         |
| reversion_version                          | revision_id                       | int NOT NULL                                         |
| reversion_version                          | db                                | varchar(191) COLLATE utf8mb4_general_ci NOT NULL     |
| social_auth_association                    | id                                | int NOT NULL                                         |
| social_auth_association                    | server_url                        | varchar(255) COLLATE utf8mb4_general_ci NOT NULL     |
| social_auth_association                    | handle                            | varchar(255) COLLATE utf8mb4_general_ci NOT NULL     |
| social_auth_association                    | secret                            | varchar(255) COLLATE utf8mb4_general_ci NOT NULL     |
| social_auth_association                    | issued                            | int NOT NULL                                         |
| social_auth_association                    | lifetime                          | int NOT NULL                                         |
| social_auth_association                    | assoc_type                        | varchar(64) COLLATE utf8mb4_general_ci NOT NULL      |
| social_auth_association                    | id                                | int NOT NULL                                         |
| social_auth_association                    | email                             | varchar(254) COLLATE utf8mb4_general_ci NOT NULL     |
| social_auth_association                    | code                              | varchar(32) COLLATE utf8mb4_general_ci NOT NULL      |
| social_auth_association                    | verified                          | tinyint(1) NOT NULL                                  |
| social_auth_association                    | timestamp                         | datetime(6) NOT NULL                                 |
| social_auth_association                    | id                                | int NOT NULL                                         |
| social_auth_association                    | server_url                        | varchar(255) COLLATE utf8mb4_general_ci NOT NULL     |
| social_auth_association                    | timestamp                         | int NOT NULL                                         |
| social_auth_association                    | salt                              | varchar(65) COLLATE utf8mb4_general_ci NOT NULL      |
| social_auth_association                    | id                                | int NOT NULL                                         |
| social_auth_association                    | token                             | varchar(32) COLLATE utf8mb4_general_ci NOT NULL      |
| social_auth_association                    | next_step                         | smallint UNSIGNED NOT NULL                           |
| social_auth_association                    | backend                           | varchar(32) COLLATE utf8mb4_general_ci NOT NULL      |
| social_auth_association                    | data                              | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| social_auth_association                    | timestamp                         | datetime(6) NOT NULL                                 |
| social_auth_usersocialauth                 | id                                | int NOT NULL                                         |
| social_auth_usersocialauth                 | provider                          | varchar(32) COLLATE utf8mb4_general_ci NOT NULL      |
| social_auth_usersocialauth                 | uid                               | varchar(255) COLLATE utf8mb4_general_ci NOT NULL     |
| social_auth_usersocialauth                 | extra_data                        | longtext COLLATE utf8mb4_general_ci NOT NULL         |
| social_auth_usersocialauth                 | user_id                           | int NOT NULL                                         |
| social_auth_usersocialauth                 | created                           | datetime(6) NOT NULL                                 |
| social_auth_usersocialauth                 | modified                          | datetime(6) NOT NULL                                 |
