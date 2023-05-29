# Interfaces
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
return: msg replies_sorted_by_time replies_sorted_by_like
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