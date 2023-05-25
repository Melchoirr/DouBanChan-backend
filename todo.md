* media

  * 上传图片
  * 热度排名，需要按照访问增加热度
  * 发表评论
  * media-chat : 话题的tag

* user

  * login直接返回user.todict()

* chat

  * 列表
    * 返回所有的chat，怎样统计热度？
  * 详细
    * 返回下属text

* post

  * 是举报帖子还是举报text
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
  * 数据表
    * id
    * 话题
    * 标题
    * 代表text
    * 自己的赞和踩
    * 时间
    * 热度？

* text

  * 数据表
    * 楼层
    * 所属post

* group

  * 表

    * tag（科技，生活...）

  * 列表

    * 返回所有的chat，怎样统计热度？

    