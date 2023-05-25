# Interfaces
```
group = [
    chat = [
        tiezi = [
            text(1)
            text
                text
                text
                ...
            ...
        ]
        ...
    ]
    ...
]
```
## base
### 
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
### 更改头像

### query single user

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
### like

### dislike

### 想看

### 在看

### 看过

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
### 加入话题

### 退出话题

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
### 添加话题

### 加入小组

### 退出小组

### 申请成为管理员

### 更改头像

## picture
### upload single picture
```
url:    /picture/upload
param:  p_content
return: msg picture
```
## text
### 发评论

### 删评论

### 点赞评论

### 点踩评论

## 帖子
### query single 帖子
