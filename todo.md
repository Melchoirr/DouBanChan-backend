* chat

  * 列表
    * 返回所有的chat，怎样统计热度？
  * 详细
    * 返回下属text

* post

  * 是举报帖子还是举报text:all
  * 发帖
  * 回帖
  * 回复
  * 返回：
    * 列表：
      * id
      * 代表text
      * 按照时间或者热度排序
    * 详细
      * 下属text数组，按照楼层排序

* group

  * 列表

    * 小组（filter by 某些tag）
    * 这些小组的post

    

* user
  * *登出时需要前端将uid设置成0，logout作废*
  
* media
  * 
  
* chat
  * add post
  * reply post
  * delete post
  * 

* 富文本

* 上传图片要返回url

* 

* 

* text需要t_topic？

* post和text返回user需要todict（显示发表该内容的用户信息），只要不返回manytomany就行

* group下addpost和chat下addpost

* manytomany怎么添加项？

  * 在中间表添加（推荐）
  * 在一端添加（不方便设置中间表属性）

* 创建帖子 需要在框里面输入新话题或者选择下拉列表里面的话题

  * 新输入话题，就先addchat（单独按钮）
  * 所有都需要request.chat

* reply post算加入话题吗？算，在主页显示，

* 小组详情页展示帖子，设置精华，置顶

* group下的post：post的group键

* 想看，在看，看过要不要在页面标记出来？

* 检查todict：有外键todict的，none的，需要特殊处理，初值尽量不要none
* 单独更新信息
* 只有chat需要heat，其他的都有自己的热度键
* media delete comment
* 所有delete还需要检查是否是系统管理员
  * 级联删除？
  * 一楼和post的双向引用
* 检查post是否点赞，只能在post详情页操作或者显示
* user-user键？
* query single 不完备











