"""
Classes defining the user network.
This is implemented as a graph:
each "user" is a vertex of the "user_network" graph.
The routine "add_friend" will add an edge to the graph.
Similarly, the routine "del_friend" removes an edge.
"""

class user:
    """
    Contains the definition of a user.
    
    -------------
    Attributes:
    id: str, user id.
    friends: set, user friends.
        Friends change constantly, and therefore a "set" type is appropriate, as it allows for constant changes.
    social_network: list, social network of user.
        This list is redefined every time the social_network changes.
        The degree of social network is set in the variable "social_network.network_degree" 
    """
    def __init__(self,key):
        """
        Initialize a user with zero friends and no social network.
        """
        self.id = key
        self.friends = set()
        self.social_network=[]

class user_network:
    """
    Graph object containg the user network.

    -------------
    Attributes:
    user_list: dic, dictionary that contains a user_list. 
        The dictionary has as keys the user ids
        and "user" objects as values.

    num_users: int, number of users in the user_list
    network_degree: int, degree defining the size of the 
       friends networks.
    tracked_number_of_purchases: int, parameter that tells
       number of purchases of the users network to keep track

    ------------
    Methods:
    add_friend
    add_user
    del_friend
    if_notpresent_add_user
    get_friends_of_friends
    get_user
    get_users
    show_social_networks 
    update_friend_list
    """
    def __init__(self):
        """
        Initialize the user network with an empty dictionary, zero users and network_degree of 2.
        """
        self.user_list = {}
        self.num_users = 0
        self.network_degree=2
        self.tracked_number_of_purchases=0 

    def add_user(self,key):
        """
        Adds a user to the network.
        The new user is identified by a key (user ID).
        "num_users" variable is increased by 1.

        -------------
        Arguments
        key, str: user ID
        """
        self.num_users = self.num_users + 1
        new_user = user(key)
        self.user_list[key] = new_user

    def if_notpresent_add_user(self,key):
        """
        Verify if user is already defined in the network.
        If not present, this calls "add_user" to add it.

        -------------
        Arguments
        key, str: user ID
        """
        if ( not self.__contains__(key) ):
            self.add_user(key)

    def get_user(self,key):
        """
        Returns the user object for a given key.

        -------------
        Arguments
        key, str: user ID
        """
        if ( self.__contains__(key) ):
            return self.user_list[key]
        else:
            return None

    def __contains__(self,key):
        """
        Checks condition: if user is contained in the network.

        -------------
        Arguments
        key, str: user ID

        -------------
        Output
        Returns True or False, for condition above.
        """
        return key in self.user_list

    def add_friend(self,user1,user2):
        """
        Adds "user2" to the set of friends of "user1"

        -------------
        Arguments
        user1, str: user ID
        user2, str: user ID

        -------------
        Side effects
        If users are not defined, add them to the network.
        """

        # If not present add users to the network:
        self.if_notpresent_add_user(user1)
        self.if_notpresent_add_user(user2)
        # This is a bidirectional graph
        self.user_list[user1].friends.add(user2)
        self.user_list[user2].friends.add(user1)

    def del_friend(self,user1,user2):
        """
        Deletes "user2" from the set of friends of "user1"

        -------------
        Arguments
        user1, str: user ID
        user2, str: user ID

        -------------
        Side effects
        If users are not defined, add them to the network.
        """
        if user1 not in self.user_list:
            self.add_user(user1)
        if user2 not in self.user_list:
            self.add_user(user2)
        USER1=self.user_list[user1] 
        if user2 in USER1.friends :
            USER1.friends.discard(user2)
        USER2=self.user_list[user2] 
        if user1 in USER2.friends :
            USER2.friends.discard(user1)

    def get_users(self):
        """
        Returns the list of users in the network.
        """
        return self.user_list.keys()

    def update_social_network(self):
        """
        Updates social-network list for each user.
        The social network is defined by the "network_degree" variable.
        This uses a recursive algorithm to search over the set of friends of each user, a number of times defiend by the "network_degree".
 
        """

        # Iterate over users:
        user_list=self.get_users() 
        for user in user_list:
            # Initialize a friend_set consisting of the user:
            friend_set={user}
            # Then recursively find the list of friends given the parameter self.network_degree:
            for D in range(2,self.network_degree+1):
                # Get friends for the set of users in friend_set:
                new_friend_set=self.get_friends_of_friends(friend_set)
                # Add friend set found above to "friend_set"  
                friend_set=friend_set.union(new_friend_set)
                # Remove user key to its own list of Neighbors:
                friend_set.discard(user)
            self.user_list[user].social_network=list(friend_set)

    def get_friends_of_friends(self,input_friend_set):
        """
        For a given set of friends in input, this returns the set of friends of friends.
 
        ---------------
        Arguments
        input_friend_set, set, set of friends

        Output
        output_friend_set, set, set of friends of friends 
        """

        output_friend_set=input_friend_set 
        for user_id in input_friend_set:
            friend_set=self.user_list[user_id].friends
            output_friend_set=output_friend_set.union(friend_set)
        return(output_friend_set)

    def show_social_networks(self):
        """
        Prints out the social network for each user
        """
        print("Social Network for each user:")
        for user in self.get_users():
            friends=self.get_user(user).social_network
            friends=', '.join(friends)
            print("user: {0} social network: {1}".format(user,friends))
         
