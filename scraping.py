from BeautifulSoup import BeautifulSoup
import urllib2

years=["2002", "2003", "2004", "2005", "2006", "2007", "2008", "2009", "2010", "2011", "2012", "2013", "2014"]

team_dict = {'Arizona Cardinals' : 'ARI', 'Atlanta Falcons' : 'ATL', 'Baltimore Ravens' : 'BAL', 'Buffalo Bills' : 'BUF', 'Carolina Panthers' : 'CAR', 'Chicago Bears' : 'CHI', 'Cincinnati Bengals' : 'CIN', 'Cleveland Browns' : 'CLE', 'Dallas Cowboys' : 'DAL', 'Denver Broncos' : 'DEN', 'Detroit Lions' : 'DET', 'Green Bay Packers' : 'GB', 'Houston Texans' : 'HOU', 'Indianapolis Colts' : 'IND', 'Jacksonville Jaguars' : 'JAC', 'Kansas City Chiefs' : 'KC', 'Miami Dolphins' : 'MIA', 'Minnesota Vikings' : 'MIN', 'New England Patriots' : 'NE', 'New Orleans Saints' : 'NO', 'New York Giants' : 'NYG', 'New York Jets' : 'NYJ', 'Oakland Raiders' : 'OAK', 'Philadelphia Eagles' : 'PHI', 'Pittsburgh Steelers' : 'PIT', 'San Diego Chargers' : 'SD', 'San Francisco 49ers' : 'SF', 'Seattle Seahawks' : 'SEA', 'St. Louis Rams' : 'STL', 'Tampa Bay Buccaneers' : 'TB', 'Tennessee Titans' : 'TEN', 'Washington Redskins' : 'WAS'}


base_url="http://www.pro-football-reference.com/years/"
home_url="http://www.pro-football-reference.com"

#Function to scrape drive summaries, row by row
def get_drive_summary(team):
    for tag1 in team:
        try:
            if 'Drives' in tag1.h2.text:
                drive_title1=tag1.h2.text.split(' ')[:-1]
                drive_info1=tag1.text
                full_name=' '.join(word for word in drive_title1)
                print "      Fetching", full_name 
                team_abbrev=team_dict.get(full_name)
                driverows=[]
                rows = tag1.findChildren(['th', 'tr'])

                for row in rows:
                    cells = row.findChildren('td')
                    for cell in cells:
                        value = cell.string
                        driverows.append(value)

                drive_no=0
                quarter=1
                time=2
                los=3
                duration=5
                yards=6
                result=7
                
                while result < len(driverows):
                    with open(teamdrivesoutputfile, 'a') as fileteamdrives:
                        fileteamdrives.write(''.join(team_abbrev + "," + str(driverows[drive_no]) + "," + str(driverows[quarter]) + "," +  str(driverows[time]) + "," + str(driverows[los]) + "," + str(driverows[duration]) + "," + str(driverows[yards]) + "," + str(driverows[result]) + "\n"))
                        drive_no+=9
                        quarter+=9
                        time+=9
                        los+=9
                        duration+=9
                        yards+=9
                        result+=9
                
        except AttributeError:
            continue

##First, get all of the links for the box scores
for year in years:
    link_library=[]
    year_url=''.join([base_url, year, "/games.htm"])
    page=urllib2.urlopen(year_url)
    soup=BeautifulSoup(page)
    for a in soup.findAll('a'):
        if 'boxscore' in a['href']:
            if 'htm' in a['href']:
                link_library.append(a['href'])
    
##Now iterate through each boxscore
    for game in link_library:
        boxscore_url=''.join([home_url, game])
        print boxscore_url
        game_id = boxscore_url[-16:-4]
        page=urllib2.urlopen(boxscore_url)
        soup=BeautifulSoup(page)
        teamdrivesoutputfile=''.join(year + '/' + game_id + "_drives.csv")

##Now grab both home and away drive summaries
        print "    Grabbing Drive Info..."
        team1 = soup.findAll("div", { "class" : "float_left" })
        team2 = soup.findAll("div", { "class" : "float_left margin_left" })
        get_drive_summary(team1)
        get_drive_summary(team2)