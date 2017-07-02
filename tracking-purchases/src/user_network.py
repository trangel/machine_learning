debug=False

class user:
    def __init__(self,key):
        self.id = key
        self.friends = set() #set
        self.social_network=[]

class user_network:
    def __init__(self):
        self.user_list = {}
        self.num_users = 0
        self.network_degree=2 #Initizalize as 2
        self.tracked_number_of_purchases=0

    def add_user(self,key):
        self.num_users = self.num_users + 1
        new_user = user(key)
        self.user_list[key] = new_user

    def if_notpresent_add_user(self,key):
        if key not in self.user_list:
            self.add_user(key)

    def get_user(self,n):
        if n in self.user_list:
            return self.user_list[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.user_list

    def add_friend(self,user1,user2):
        # If not present add users to the network:
        self.if_notpresent_add_user(user1)
        self.if_notpresent_add_user(user2)
        # This is a bidirectional graph
        self.user_list[user1].friends.add(user2)
        self.user_list[user2].friends.add(user1)
        if ( debug ):
            print("{} and {} are now friends".format(user1,user2))

    def del_friend(self,user1,user2):
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
        if ( debug ):
            print("{} and {} are no longer friends".format(user1,user2))

    def get_users(self):
        return self.user_list.keys()

    def __iter__(self):
        return iter(self.user_list.values())

    def update_friend_list(self):
        user_list=self.get_users()
        for user in user_list:
            # Initialize a Nrb set with the user:
            friend_set={user}
            # Then recursively find the list of friends given the parameter self.network_degree:
            for D in range(2,self.network_degree+1):
                # Get friends for the set of users in friend_set:
                new_friend_set=self.get_friends(friend_set)
                # Add friend set found above to "friend_set"  
                friend_set=friend_set.union(new_friend_set)
                # Remove user key to its own list of Neighbors:
                friend_set.discard(user)
            self.user_list[user].social_network=list(friend_set)

    def get_friends(self,input_friend_set):
        output_friend_set=set() 
        for user_id in input_friend_set:
            friend_set=self.user_list[user_id].friends
            output_friend_set=input_friend_set.union(friend_set)
        return(output_friend_set)

    def show_social_networks(self):
        print("Social Network for each user:")
        for user in self.get_users():
            friends=self.get_user(user).social_network
            friends=', '.join(friends)
            print("user: {0} friends: {1}".format(user,friends))
         
