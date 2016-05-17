class AccountMeta:
    META = {
        '新用户': 20,
        '分享链接': 5,
        '收藏链接': 1,
        '分享被收藏': 1,
        '选入每日推荐': 10,
        '选入专题': 50,
        '留言': 1,
        '评论': 1,
        '取消收藏': -2,
        '分享链接被移除': -10,
        '强制阅读': -10,
    }
    META_LIST = sorted([{'info': k, 'acc': v} for k, v in META.items()], key=lambda k: k['acc']*-1)