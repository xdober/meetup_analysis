class Const:
    EVENT_PATH = 'data/events.csv'
    GROUP_PATH = 'data/groups.csv'
    CITY_PATH = 'data/cities.csv'
    CTGY_PATH = 'data/categories.csv'
    TOPIC_PATH = 'data/topics.csv'
    GRP_TPC_PATH = 'data/groups_topics.csv'
    MEMBER_PATH = 'data/members.csv'
    MMB_TPC_PATH = 'data/members_topics.csv'
    VENUE_PATH = 'data/venues.csv'
    GROUP_PER_MEMBER = 'result/group_number_per_member.csv'
    MEMBER_PER_GROUP = 'result/member_per_group.csv'
    class ConstError(TypeError):
        pass

    class ConstCaseError(ConstError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't change const value!")
        if not name.isupper():
            raise self.ConstCaseError('const "%s" is not all letters are capitalized' % name)
        self.__dict__[name] = value


import sys

sys.modules['Const'] = Const()

# Const.EVENT_PATH = 'data/events.csv'
# Const.GROUP_PATH = 'data/groups.csv'
# Const.CITY_PATH = 'data/cities.csv'
# Const.CTGY_PATH = 'data/categories.csv'
# Const.TOPIC_PATH = 'data/topics.csv'
# Const.GRP_TPC_PATH = 'data/groups_topics.csv'
# Const.MEMBER_PATH = 'data/members.csv'
# Const.MMB_TPC_PATH = 'data/members_topics.csv'
# Const.VENUE_PATH = 'data/venues.csv'
# Const.GROUP_PER_MEMBER = 'result/group_number_per_member.csv'
# Const.MEMBER_PER_GROUP = 'result/member_per_group.csv'
