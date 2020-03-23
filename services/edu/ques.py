from models import edu 


def nextQuestion():
	l = edu.Page.objects.all()
	print len(l)
	return l
