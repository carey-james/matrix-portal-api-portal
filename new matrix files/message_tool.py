def message_tool(text):
	text = str(text)
	if len(text) > 12:
		text = f'{text [0:10]}…'
	return text