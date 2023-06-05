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

* 不能重复的问题

  * 点赞
  * 评分
  * 加入小组（发申请可以很多次）

* is_self字段

* 修改char的max_length

* 在小组里 

* 访问其他小组帖子

* 判断：是不是管理员

* 删除按钮：小组管理员想通过访问话题访问道了自己的小组，要显示删帖按钮

  * （限制只能在小组页面删除）
  * （按下“管理”之后才开始显示删除按钮）
  * 或者需要在返回的时候加一个是否是管理员的key以及一个是否是本人（不必要）的key

* 整理一下大管理员需要做的事情

* 需要在小组公共区显示

  * 一个小组 有人在申请
  * 改掉全部的 usergroup

* 返回人

* 需要判断管理员身份的时候？

  * 踢人
  * 同意申请
  * 返回post的时候判断
  
* 热度键重新维护

  * media
  * 影评
  * chat
  * post
  * 楼层



* 消息

  * 返回消息总数
  * 返回3个列表

    * 点赞

      * post
      * text

    * 回复

      * text回复

    * 这两个都是：post/text id + uid，支持跳转（甚至不需要后端操作）
    * 系统

      * 申请管理员成功
      * 申请管理员失败

        * 小组

      * 被举报
      * 被删除

        * 

      * 举报成功
      * 举报失败

    * 返回列表只需要分三类，返回每一条的时候在todict里面写if，接收的时候直接创建，也分三类就行
    * 处理举报

* 小组详情页返回：is_member, is_group_admin
* 返回post，text返回：is_self, is_group_admin
* 设置精华无需额外判断
* 返回的时候参考

* 重写某些tostring
* 





