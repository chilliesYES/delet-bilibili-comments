感谢https://www.aicu.cc/提供的api

目前找到自己账号的评论数据有如下三种：1.通过aicu查询获取（不是最新的，需要等站长更新）2.被回复评论通过api查3.被赞评论通过api查

目前本脚本实现前两种的查询上传和删除，结合mysql可以对自己的评论数据留档，但是请注意你删除的评论无论是在b站还是aicu依旧存在，删除评论只是不再让弱智打扰你

sql数据库结构
#  | 名字     | 类型           | 排序规则             | 属性 | 空  | 默认  | 注释 | 额外           
---|----------|----------------|----------------------|------|-----|--------|------|----------------
1  | id       | int(11)        |                      |      | 否  | 无     |      | AUTO_INCREMENT
2  | id1      | int(11)        |                      |      | 是  | NULL   |      |                
3  | message  | varchar(1000)  | utf8mb4_general_ci   |      | 是  | NULL   |      |                
4  | zan      | int(6)         |                      |      | 是  | NULL   |      |                
5  | rpid     | char(20)       | utf8mb4_general_ci   |      | 是  | NULL   |      |                
6  | oid      | char(20)       | utf8mb4_general_ci   |      | 是  | NULL   |      |                
7  | t        | bigint(15)     |                      |      | 是  | NULL   |      |                
8  | status   | int(1)         |                      |      | 是  | 0      |      |                

使用方法：
使用前需要在config文件里把你的csrf和cookies和user-agent填进去。
csrf的位置:在个人主页打开f12 cookie选项下找到bili_jct字段就是csrf（以后有心情做扫码）
config里还有sql数据库的相关信息也得填，如不想用mysql得自己改
go_del下有个start(9999,1)可以不动，第一个是上限第二个是下限，如果中途有中断在his.txt里可以找到中断位置(第一遍是这么写的懒得改了)
如果你是从aicu获取数据那就把json放jsont下，如果是从b站api获取直接运行main就行了
由于aicu的api有机器验证强烈建议手点api改参数通过复制粘贴的方式把数据弄出来

目前可能有一些bug凑合用吧
