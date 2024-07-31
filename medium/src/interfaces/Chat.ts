export interface ChatState {
	chats: Chat[];
}

export interface Chat {
	id: string,
	systemMsg?: string,
	userMsg?: string
	room: string
	name: string
}