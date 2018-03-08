import rakeUsingSpacy
sample_file=open("/home/login/Scapy Intent Detection/1.txt")
text=sample_file.read()
rake_object=rakeUsingSpacy.Rake()
keywords=rake_object.run(text)
print "Keywords:",keywords[:20]