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
### change profile photo

### query single user
```
url:    /user/query_single
param:  u_id
return: msg user
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
url:    /media/delet
param:  m_id
return: msg
```
### query single media
```
url:    /media/query_single
param:  m_id
return: msg media text_by_time text_by_like
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
## chat
### create chat
```
url:    /chat/create
param:  c_name c_description
return: msg chat
```
### delete chat
```
url:    /chat/create
param:  c_id
return: msg
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
## group
### create group
```
url:    /group/create
param:  g_name g_description
return: msg group
```
### delete group
```
url:    /group/delete
param:  g_id
return: msg
```
### query single group
```
url:    /media/query_single
param:  g_id
return: msg group
```
### add chat

### join group

### quit group

### apply to be admin of group

### change group profile photo

## picture
### upload single picture
```
url:    /picture/upload
param:  p_content
return: msg picture
```
## text
### post text

### delete text

### like text

### dislike text

## post
### query single post
