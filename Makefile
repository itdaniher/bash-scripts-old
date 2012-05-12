me:
	@true
a:
	@true
sandwich:
	@[ -w /etc/shadow ] && echo "Okay." || echo "What? Make it yourself."
