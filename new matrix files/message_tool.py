def message_tool(text):
	text = str(text)
	if len(text) > 12:
		text = f'{text [0:10]}…'
	return text

def middle_pad(left_text, right_text):
	left_text = str(left_text)
	right_text = str(right_text)
	spaces = '            '
	if len(left_text) + len(right_text) < 12:
		full_text = f'{left_text}{spaces[0:(12 - (len(left_text) + len(right_text)))]}{right_text}'
	else:
		full_text = message_tool(f'{left_text} {right_text}')
	return full_text