# Interfaces
[toc]
Return value

* media

  ```
  media = {
              'm_id'
              'm_name'
              'm_type'
              'm_rate'
              'm_rate_num'
              'm_genre'
              'm_description'
              'm_year'
              'm_region'
              'm_director'
              'm_actor'
              'm_episode_num'
              'm_duration'
              'm_author'
              'm_characters'
          }
  ```

* chat

  ```
  chat = {
              'c_id'
              'c_name'
              'c_description'
              'c_create_time'
              'c_last_modify_time'
              'c_heat'
              'c_profile_photo'
              'c_father_group'
          }
  ```

* group

  ```
  group = {
              'g_id'
              'g_name'
              'g_description'
              'g_create_time'
              'g_last_modify_time'
              'g_users_num'
              'g_tag'
              'g_profile_photo'
              
          }
  ```

* picture

  ```
  picture {
              'p_id'
              'p_content'
          }
  ```

* report

  ```
  report {
              'r_id'
              'r_user'
              'r_text'
              'r_details'
          }
  ```

* text

  ```
  text = {
              't_id'
              't_type'
              't_topic'
              't_user'
              't_rate'
              't_like'
              't_dislike'
              't_description'
              't_create_time'
              't_media'
              't_floor'
              't_post'
          }
  ```

* user

  ```
  user = {
              'u_id'
              'u_name'
              'u_email'
              'u_profile_photo'
          }
  ```

* post

  ```
  post = {
              'p_id'
              'p_user'
              'p_title'
              'p_like'
              'p_dislike'
              'p_chat'
              'p_first_floor_text'
              'p_create_time'
              'p_floor_num'
              'p_is_essence'
              'p_is_top'
              'p_group'
          }
  ```

  

## base

### query base
```
url:    /base/query_base
param:  qstr
return: msg data
```
### query user
```
url:    /base/query_user
param:  qstr
return: msg data
```
### query chat
```
url:    /base/query_chat
param:  qstr
return: msg data
```
### query group
```
url:    /base/query_group
param:  qstr
return: msg data
```
### query media
```
url:    /base/query_media
param:  qstr
return: msg data
```
### query report
```
url:    /base/query_report
param:  qstr
return: msg data
```
## user
### register
```
url:    /user/register
param:  username password
return: msg user
```
### login
```
url:    /user/login
param:  username password
return: msg
```
### logout
```
url:    /user/logout
param:  
return: msg
```
### update user

```
```

### change profile photo

```
url:    /user/upload_profile
param:  u_id p_content
return: msg
```

### query single user
```
url:    /user/query_single
param:  u_id
return: msg user
```
### user home

```

```

## media

### create media
```
url:    /media/create
param:  m_name m_type m_genre m_description m_year m_director m_actor m_episode_num m_duration m_author m_characters 
return: msg
```
### delete media
```
url:    /media/delete
param:  m_id
return: msg
```
### query single media
```
url:    /media/query_single
param:  m_id
return: msg media text_by_time text_by_like m_chats
```
### media filter
```
url:    /media/filter
param:  m_type m_genre m_region m_year m_order
return: msg media
```
### media add preview
```
url:    /media/add_preview
param:  m_id p_id
return: msg
```
### media home

```
```

### set to be watched
```
url:    /media/set_to_be_watched
param:  m_id op
return: msg
```
### set watching
```
url:    /media/set_watching
param:  m_id op
return: msg
```
### set watched
```
url:    /media/set_watched
param:  m_id op
return: msg
```
### set favourite
```
url:    /media/set_favourite
param:  m_id op
return: msg
```
### comment_media

```
```

### rate_media

```
```

### like_comment

```
```

### dislike_comment

```
```

## chat

### create chat
```
url:    /chat/create
param:  c_name c_description u_id [c_profile_photo group]
return: msg chat
```
### delete chat
```
url:    /chat/create
param:  c_id
return: msg
```
### chat home

```
```

### query single chat

```
url:    /chat/query_single
param:  c_id
return: msg chat
```
### join chat
```
url:    /chat/join_chat
param:  c_id
return: msg
```
### quit chat
```
url:    /chat/quit_chat
param:  c_id
return: msg
```
### add post (发帖)

```
```

### reply post (回帖)

```
```

### like post

```
```

### dislike post

```
```

### delete post

```
```

## group
### create group
```
url:    /group/create
param:  g_name g_description
return: msg group
```
### update group

```
没有改变的键也要按原样发送过来
```

### delete group

```
url:    /group/delete
param:  g_id
return: msg
```
### group home

```
```

### query single group

```
url:    /media/query_single
param:  g_id
return: msg group
```
### add post (发帖)

```
```

### add chat

```
```

### join group

```
```

### quit group

```
```

### set essence

```
```

### set top

```
```

### apply admin

```
```

### grant admin

```
```

### 

## picture
### upload single picture 
```
url:    /picture/upload
param:  p_content
return: msg picture
```
## text
### query single text
```
url:    /text/query_single
param:  t_id
return: msg text replies_sorted_by_time replies_sorted_by_like
```
### reply text (回复)
```
url:    /text/reply
param:  t_description t_father_text_id
return: msg text
```
### delete text
```
url:    /text/delete
param:  t_id
return: msg
```
### like text
```
url:    /text/like
param:  t_id
return: msg
```
### dislike text
```
url:    /text/dislike
param:  t_id
return: msg
```
## post
### query single post
```
url:    /post/query_single
param:  p_id
return: msg post text_by_floor
```
### like post

### dislike post

### add text
```
url:    /post/add_text
param:  t_description t_topic t_post_id t_floor
return: msg text
```
## report
### add report
```
url:    /report/add_report
param:  t_id r_details
return: msg report
```
### delete report
```
url:    /report/delete_report
param:  r_id
return: msg
```
### query single report
```
url:    /report/query_single
param:  r_id
return: msg report
```