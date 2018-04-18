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
    REAL_MEMBER_PATH='data/real_members.csv'
    GROUP_PER_MEMBER = 'result/group_number_per_member.csv'
    MEMBER_PER_GROUP = 'result/member_per_group.csv'
    SIMPLE_PATH = 'result/simple.csv'
    E_M_GROUP_PATH = 'result/event_member_per_group.csv'
    E_M_CATE_PATH = 'result/event_member_per_category.csv'
    ART_EVENT_PATH = 'result/Arts_event_mean.csv'
    CAREER_EVENT_PATH = 'result/Career_event_mean.csv'
    BOOK_EVENT_PATH = 'result/Book_event_mean.csv'
    ART_EVENT_DATA_PATH = 'result/art_event_data.csv'
    CAREER_EVENT_DATA_PATH = 'result/career_event_data.csv'
    BOOK_EVENT_DATA_PATH = 'result/book_event_data.csv'
    TOPIC_SUBTOPIC_PATH = 'result/subTopic and member.csv'
    TPC_GRPBY_PATH = 'result/topic groupby topic.csv'
    TPC_GRP_GRPBY_PATH = 'result/topic groupby topic and group.csv'
    TPC_GRP_TPC_PATH = 'result/maintopic groupby topic.csv'
    CATE_TOPIC_PATH = 'result/groups number per category per main topic.csv'
    TPC_GRP_NUM_MEM = 'result/topic and group number per member.csv'
    MEM_JOIN_GRP_TINY = 'data/member_join_group_tiny.csv'
    MEM_JOIN_GRP_MID = 'data/member_join_group.csv'
    MEM_NO_DUMP = 'data/members_no_dump.csv'
    MEM_TPC_TINY = 'data/member_topic_tiny.csv'

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
