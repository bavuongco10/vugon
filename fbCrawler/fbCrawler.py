import unittest
from alltest.places import Places
from alltest.likes import Likes
from alltest.events import Events
from alltest.groups import Groups
from alltest.reviews import Reviews

class FbCrawler(unittest.TestSuite):
    
    def suite():
        suite= unittest.TestSuite()
        suite.addTest(VisitedPlaces('test_visitedPlaces'))
        suite.addTest(Likes('test_likes'))
        suite.addTest(Events('test_events'))
        suite.addTest(Groups('test_groups'))
        suite.addTest(Reviews('test_reviews'))
        return suite
        
    if __name__ == "__main__":
        #unittest.TextTestRunner().run(suite()) 
        unittest.main()
