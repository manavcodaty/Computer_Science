APP_NAME = CruiseShipBooking
SOURCE = main.m

.PHONY: all run clean

all: $(APP_NAME)

$(APP_NAME): $(SOURCE)
	clang -fobjc-arc -framework Foundation $(SOURCE) -o $(APP_NAME)

run: $(APP_NAME)
	./$(APP_NAME)

clean:
	rm -f $(APP_NAME)
