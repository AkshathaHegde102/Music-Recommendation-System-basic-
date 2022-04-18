DATABASE_NAME = "music.txt"


def title(name: str):
    """
        get username as input, return formatted names
        example: eminem -> Eminem, TMBG -> Tmbg, Kerkylas of Andros -> Kerkylas Of Andros
        @author: Jinming Shi
    """
    name_arr = map(lambda x: x.lower(), name.split())
    return ' '.join(map(lambda x: x[0].upper() + x[1:], name_arr))


def loadUsers(filename):
    """ Reads the content in file and places it into a dictionary
        @author: Jinming Shi """
    dictionary = {}
    try:
        with open(filename, "r") as fp:
            for line in fp:
                [user, singers] = line.strip().title().split(":")
                singersList = singers.split(",")
                singersList.sort()
                dictionary[user] = singersList
        return dictionary
    except FileNotFoundError:
        fp = open(DATABASE_NAME, 'w')
        return dictionary


def enterPreference(userName, userDict):
    """  ask user enter preference until empty
        @author: Jinming Shi """
    # Instead of replacing the old preferences, add them to the existing list
    if userName in userDict:
        prefs = userDict[userName]
        newPref = input("Enter an artist that you like (Enter to finish):")
    else:
        prefs = []
        newPref = input("Enter an artist that you like (Enter to finish):")

    while newPref != "":
        prefs.append(newPref.strip().title())
        newPref = input("Enter an artist that you like (Enter to finish):")

    # Always keep the lists in sorted order for ease of comparison
    prefs = list(set(prefs))
    prefs.sort()
    return prefs


def numMatches(userPrefs, prevUserPrefs):
    '''Compares the current preferences to a previous preference list
        and returns the number of matches and Will compare and return
        the values not matching. LEARNT IN CLASS
        This is a helper function
        @author : Akshatha Vasant Hegde '''
    matchList = []
    newList = []
    x = list(userPrefs)
    x.sort()
    y = list(prevUserPrefs)
    y.sort()
    i, j, cnt = 0, 0, 0
    while i < len(x) and j < len(y):
        if x[i] == y[j]:
            i += 1
            j += 1
            cnt += 1
        elif x[i] < y[j]:
            i += 1
        else:
            newList = newList + [y[j]]
            j += 1
    newList = newList + prevUserPrefs[j:]
    return cnt, newList


def getRecommendations(userName, Preferences, userDict):
    '''Compares the Preferences of your user to the users in userDict.
        for the user with the maximum nuber of matches, return the rest of the
        peferences as a recommendation without the original recommendations
        @author: Akshatha Vasant Hegde
        '''
    # BUG FIXED
    BestNum = 0
    BestUser = ""
    for prev_user in userDict.keys():
        if prev_user[-1] == '$':
            continue  # for excluding the private users
        prev_user_pref = userDict[prev_user]
        matchCnt, x = numMatches(Preferences, prev_user_pref)
        if matchCnt > BestNum:
            if matchCnt == len(prev_user_pref):
                continue  # make sure that empty list is not given
            BestNum = matchCnt
            BestUser = prev_user
    if BestNum == 0:
        print("No recommendations available at this time .")
        return []
    print("Your recommendations are : ")
    a, Rec = numMatches(Preferences, userDict[BestUser])
    return Rec


def findTopArtists(userDict):
    '''Finds the Top 3 most popular artists in a List.
        @author: Akshatha Vasant Hegde
        '''
    newList = []
    Top = []
    Count, Freq, Counter = 0, 0, 3
    BestArtist = ""
    for prev_user in userDict.keys():
        if prev_user[-1] == '$':
            continue  # for excluding the private users
        newList = newList + userDict[prev_user]
    for w in range(3):
        for i in newList:
            Count = newList.count(i)
            if Count > Freq:
                Freq = Count
                BestArtist = i
        Top = Top + [BestArtist]
        for num in range(Count):
            newList.remove(BestArtist)
        Count, Freq = 0, 0
    if (Top == []):
        return ("Sorry , no artists found.")
    return Top


def findLikes(userDict):
    '''Finds the likes of the most popular artist.
        @author: Akshatha Vasant Hegde
        '''
    newList = []
    freq, cnt = 0, 0
    artist = ""
    for prev_user in userDict.keys():
        if prev_user[-1] == '$':
            continue  # for excluding the private users
        newList = newList + userDict[prev_user]
    for i in newList:
        freq = newList.count(i)
        if freq > cnt:
            cnt = freq
            artist = i
    if (cnt == 0):
        return ("Sorry , no artists found.")
    return cnt, artist


def findUserLikeMostArtists(userName, userDict):
    """Return the name of the user who likes the most artists.
        @Author: Ning Zhang"""
    maxNum = 0
    targetUser = ''
    for user in userDict:
        if user[-1] == '$':
            continue  # for excluding the private users
        elif user == userName:
            continue  # for excluding the current user
        if len(userDict[user]) > maxNum:
            maxNum = len(userDict[user])
            targetUser = str(user)
    return targetUser


def saveUserPreferences(userName, prefs, userDict, fileName):
    """ Writes all the user preferences to the file.
        Returns nothing.
        @Author: Ning Zhang"""
    userDict[userName] = prefs
    file = open(fileName, "w")
    for user in userDict:
        toSave = str(user) + ":" + ",".join(userDict[user]) + "\n"
        file.write(toSave)
    file.close()


def main():
    """ The main recommendation function """

    userDict = loadUsers(DATABASE_NAME)  # gives a dictionary of users and preferences

    user_name = input("Enter your name (put a $ symbol after your name if "
                      "you wish your preferences to remain private):")
    if user_name in userDict:
        Preferences = userDict[user_name]
        print(','.join(Preferences))
    else:
        Preferences = enterPreference(user_name, userDict)
    #userDict[user_name] = Preferences

    while True:
        menu_selection = input("Enter a letter to choose an option:\n"
                               "e - Enter preferences\n"
                               "r - Get recommendations\n"
                               "s - Show Preferences\n"
                               "p - Show most popular artists\n"
                               "h - How popular is the most popular\n"
                               "m - Which user has the most likes\n"
                               "d - Remove Preferences\n"
                               "q - Save and quit\n").lower()

        if menu_selection not in ['e', 'r', 'p', 'h', 'm', 'q', 's', 'd']:
            continue

        elif menu_selection == 'e':
            """
            Enter Preferences
            @author: Jinming Shi
            """
            Preferences = enterPreference(user_name, userDict)
            # print("The users preferences are : ")
            # print(','.join(Preferences))q
            userDict[user_name] = Preferences
        elif menu_selection == 's':
            """
            Print the most up-to-date list
            @author: Jinming Shi
            """
            for name in Preferences:
                print(name)
        elif menu_selection == 'r':
            """
            Get recommendations
            @author: Akshatha Vasant Hegde
            """
            if user_name in userDict:
                del userDict[user_name]
            if Preferences == []:
                print("No recommendations available at this time .")
                continue
            Recs = getRecommendations(user_name, Preferences, userDict)
            for i in Recs:
                print(i)
            userDict[user_name] = Preferences

        elif menu_selection == 'p':
            """
            Show top 3 most popular artists
            @author: Akshatha Vasant Hegde
            """
            userDict[user_name] = Preferences
            Artists = findTopArtists(userDict)
            Artists = list(set(Artists))
            for i in Artists:
                print(i)
            del userDict[user_name]

        elif menu_selection == 'h':
            """
            How popular is the most popular artist
            @author: Akshatha Vasant Hegde
            """
            userDict[user_name] = Preferences
            Likes, Artist = findLikes(userDict)
            print(Likes)
            del userDict[user_name]
            
        elif menu_selection == 'm':
            """
            Which user has the most likes
            @author: Ning Zhang
            """
            targetUser = findUserLikeMostArtists(user_name, userDict)
            if not targetUser:
                print("Sorry , no user found.")
            else:
                print(targetUser)

        elif menu_selection == 'd':
            """
            delete user's preference by index
            @author: Ning Zhang
            """
            print("Your current preferences are:")
            for index in range(len(Preferences)):
                print(index, Preferences[index])
            artistIndex = input("Enter the number of artist which you wanna to delete:\n")
            artistIndex = int(artistIndex)
            Preferences.pop(artistIndex)

        elif menu_selection == 'q':
            """
            Save and quit
            @author: Ning Zhang
            """
            if not Preferences:
                print("You should enter preferences first!")
                continue
            else:
                saveUserPreferences(user_name, Preferences, userDict, DATABASE_NAME)
                #print('Bye,', user_name)
                break


if __name__ == '__main__':
    main()
