# Initialize variables
candidates = []
votes = []
num_candidates = 4
num_students = 30
voterID = [["Ben", "12345"], 
           ["Sarah", "password"], 
           ["Glen", "Glen123"], 
           ["Emily", "qwerty"], 
           ["Michael", "abc123"], 
           ["Olivia", "hello"], 
           ["Ethan", "password123"], 
           ["Emma", "abcdef"], 
           ["Jacob", "basketball123"],
           ["Ava", "sunshine"], 
           ["William", "football"], 
           ["Sophia", "baseball"], 
           ["James", "dragon"], 
           ["Isabella", "123456"], 
           ["Alexander", "welcome"], 
           ["Mia", "hello123"], 
           ["Logan", "admin"], 
           ["Amelia", "pass123"], 
           ["Daniel", "class135"], 
           ["Evelyn", "love"], 
           ["Liam", "secret"], 
           ["Charlotte", "12345678"],
           ["Benjamin", "p@ssw0rd"], 
           ["Abigail", "question"], 
           ["Mason", "qazwsx"], 
           ["Harper", "football123"], 
           ["Elijah", "123abc"]
                                ]      


# Get candidate names
def get_candidates():
    for i in range(num_candidates):
        candidate_name = input(f"Enter the name of candidate {i+1}: ")
        candidates.append(candidate_name)
        votes.append(0)

# Get student votes
def get_votes():
    for i in range(num_students):
        vote = input(f"{username}, enter the name of the candidate you vote for, or 'abstain' to abstain: ")
        if vote in candidates:
            index = candidates.index(vote)
            votes[index] += 1
        elif vote == 'abstain':
            continue
        else:
            print("Invalid vote, please try again.")
            i -= 1

# Calculate results
def calc_results():
    max_votes = max(votes)
    winners = []
    for i in range(len(votes)):
        if votes[i] == max_votes:
            winners.append(candidates[i])

    # Print results
    for i in range(num_candidates):
        print(f"Candidate {candidates[i]} got {votes[i]} votes.")
    if len(winners) > 1:
        print("There is a tie between the following candidates: ", ', '.join(winners))
    else:
        print("The winner is: ", winners[0])
        
        
def verify():
    print("Enter unique voter ID to vote")
    voter_id = int(input("Enter your voter ID: "))
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    if voterID[voter_id][0] == username and voterID[voter_id][1] == password:
        print("Welcome", username)
        get_votes()
        calc_results()
        return username
    else:
        print("Incorrect username or password")
        verify()

def main():
    get_candidates()
    for student in num_students:
        verify()
        get_votes()
        