import { json } from 'body-parser'
import express from 'express'
import { errorHandler } from './middlewares/error-handler';
import { Server } from "socket.io"
import { Chat } from './interfaces/Chat';
import ws from 'ws'

const server = new ws.Server({ port: 8080 })

const app = express()

import { currentPostsRouter } from './routes/posts'

app.use(json())

app.use(currentPostsRouter);
app.use(errorHandler)

const expressServer = app.listen(4000, () => {
    console.log(`listening on port 4000`)
})

const io = new Server(expressServer, {
    cors: {
        origin: ["http://localhost:8080", "http://127.0.0.1:8080"]
    }
})

const chatState = {
    chats: [] as Chat[],
    setChats: function(NewChatsArr: Chat[]) {
        this.chats = NewChatsArr
    }
}

io.on('connection', socket => {
	console.log(`User ${socket.id} connected`)

    socket.emit('message', buildMsg(`Eai, que bom te ter aqui. Ta me servindo de algo esse servidor. Comece pela pergunta que quiser.`))

    socket.on('enterRoom',({ name, room }: { name: string; room: any })  => {

        const user = activateUser(socket.id, name, room)

        socket.join(user.room);
         
    })

    socket.on('message', ({ text }) => {
        const room = getUser(socket.id)
        if (room) {
            io.to(room).emit('message', buildMsg(text))
        }
    })

    socket.on('activity', (name) => {
        const room = getUser(socket.id)
        if (room) {
            socket.broadcast.to(room).emit('activity', name)
        }
    })

})

const buildMsg = (text: string) => {
    return {
        text, 
        time: new Intl.DateTimeFormat('pt-BR', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        }).format(new Date())
    }
}

const activateUser = (id: string, name: string, room: string) => {
    const user = {id, name, room}
    chatState.setChats([
        ...chatState.chats.filter(chat => chat.id !== id),
        user
    ])
    return user
}

const getUser = (socketId: string): string | null => {
    const chat = chatState.chats.find(chat => chat.id === socketId);
    return chat ? chat.room : null; 
};

const DeactivateUser = (id: string) => {
    chatState.setChats([
        ...chatState.chats.filter(chat => chat.id !== id)
    ])
}
