from enum import Enum


class TicketClassNames(Enum):
    adult_passenger = 0
    adult_bike = 1
    child_passenger = 2
    child_bike = 3
    reduced_passenger = 4
    reduced_bike = 5

    title = 'title'
    bike = 'bike'
    subtitle = 'subtitle'
    single_fare = 'single'
    return_fare = 'return'


ticket_prices = {
    TicketClassNames.adult_passenger: {
        TicketClassNames.title: 'Erwachsener', TicketClassNames.bike: False, TicketClassNames.subtitle: 'ohne Fahrrad',
        TicketClassNames.single_fare: 150, TicketClassNames.return_fare: 250,
    },
    TicketClassNames.adult_bike: {
        TicketClassNames.title: 'Erwachsener', TicketClassNames.bike: True, TicketClassNames.subtitle: 'mit Fahrrad',
        TicketClassNames.single_fare: 200, TicketClassNames.return_fare: 300,
    },
    TicketClassNames.child_passenger: {
        TicketClassNames.title: 'Kind', TicketClassNames.bike: False, TicketClassNames.subtitle: 'ohne Fahrrad',
        TicketClassNames.single_fare: 100, TicketClassNames.return_fare: 150,
    },
    TicketClassNames.child_bike: {
        TicketClassNames.title: 'Kind', TicketClassNames.bike: True, TicketClassNames.subtitle: 'mit Fahrrad',
        TicketClassNames.single_fare: 150, TicketClassNames.return_fare: 200,
    },
    TicketClassNames.reduced_passenger: {
        TicketClassNames.title: 'Ermäßigt', TicketClassNames.bike: False, TicketClassNames.subtitle: 'ohne Fahrrad',
        TicketClassNames.single_fare: 100, TicketClassNames.return_fare: 150,
    },
    TicketClassNames.reduced_bike: {
        TicketClassNames.title: 'Ermäßigt', TicketClassNames.bike: True, TicketClassNames.subtitle: 'mit Fahrrad',
        TicketClassNames.single_fare: 150, TicketClassNames.return_fare: 200,
    },
}
