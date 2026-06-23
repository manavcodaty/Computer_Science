#import <Foundation/Foundation.h>

enum {
    TotalTables = 20,
    SessionCount = 3,
    DietaryOptionCount = 5
};

@interface Booking : NSObject
@property (nonatomic, copy) NSString *passengerName;
@property (nonatomic, copy) NSString *cabinNumber;
@property (nonatomic, copy) NSString *dietaryRequirement;
@property (nonatomic) NSInteger tableNumber;

- (instancetype)initWithPassengerName:(NSString *)passengerName
                          cabinNumber:(NSString *)cabinNumber
                    dietaryRequirement:(NSString *)dietaryRequirement
                            tableNumber:(NSInteger)tableNumber;
@end

@implementation Booking
- (instancetype)initWithPassengerName:(NSString *)passengerName
                          cabinNumber:(NSString *)cabinNumber
                    dietaryRequirement:(NSString *)dietaryRequirement
                            tableNumber:(NSInteger)tableNumber {
    self = [super init];
    if (self) {
        _passengerName = [passengerName copy];
        _cabinNumber = [cabinNumber copy];
        _dietaryRequirement = [dietaryRequirement copy];
        _tableNumber = tableNumber;
    }
    return self;
}
@end

static NSString *ReadLine(NSString *prompt) {
    printf("%s", [prompt UTF8String]);

    char buffer[256];
    if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
        return @"";
    }

    NSString *input = [NSString stringWithUTF8String:buffer];
    return [input stringByTrimmingCharactersInSet:[NSCharacterSet whitespaceAndNewlineCharacterSet]];
}

static NSInteger ReadMenuChoice(NSString *prompt, NSInteger minimum, NSInteger maximum) {
    while (YES) {
        NSString *input = ReadLine(prompt);
        NSScanner *scanner = [NSScanner scannerWithString:input];
        NSInteger choice = 0;

        if ([scanner scanInteger:&choice] && [scanner isAtEnd]) {
            if (choice >= minimum && choice <= maximum) {
                return choice - 1;
            }
            printf("Error: Please enter a number between %ld and %ld.\n", (long)minimum, (long)maximum);
        } else {
            printf("Error: Please enter a number.\n");
        }
    }
}

static NSString *ReadRequiredText(NSString *prompt, NSString *fieldName) {
    while (YES) {
        NSString *value = ReadLine(prompt);
        if ([value length] > 0) {
            return value;
        }
        printf("Error: %s cannot be empty.\n", [fieldName UTF8String]);
    }
}

static void DisplayScreen(NSArray<NSString *> *sessionNames, NSInteger tablesAvailable[]) {
    NSDateFormatter *formatter = [[NSDateFormatter alloc] init];
    [formatter setDateFormat:@"dd/MM/yyyy"];
    NSString *today = [formatter stringFromDate:[NSDate date]];

    printf("\n========================================\n");
    printf("TODAY'S DATE: %s\n", [today UTF8String]);
    printf("========================================\n");
    printf("RESTAURANT TABLE AVAILABILITY:\n");

    for (NSInteger i = 0; i < SessionCount; i++) {
        NSString *sessionName = sessionNames[i];
        if (tablesAvailable[i] == 0) {
            printf("%s: FULLY BOOKED\n", [sessionName UTF8String]);
        } else {
            printf("%s: %ld tables available\n", [sessionName UTF8String], (long)tablesAvailable[i]);
        }
    }

    printf("========================================\n");
}

static NSInteger SelectSession(NSArray<NSString *> *sessionNames) {
    printf("Select a session:\n");
    for (NSInteger i = 0; i < SessionCount; i++) {
        printf("%ld. %s\n", (long)(i + 1), [sessionNames[i] UTF8String]);
    }
    return ReadMenuChoice(@"Enter choice (1-3): ", 1, SessionCount);
}

static NSString *SelectDietaryRequirement(NSArray<NSString *> *dietaryOptions) {
    printf("\nDietary requirements:\n");
    for (NSInteger i = 0; i < DietaryOptionCount; i++) {
        printf("%ld. %s\n", (long)(i + 1), [dietaryOptions[i] UTF8String]);
    }

    NSInteger dietIndex = ReadMenuChoice(@"Select option (1-5): ", 1, DietaryOptionCount);
    return dietaryOptions[dietIndex];
}

static void MakeBooking(NSArray<NSString *> *sessionNames,
                        NSArray<NSString *> *dietaryOptions,
                        NSMutableArray<NSMutableArray<Booking *> *> *bookings,
                        NSInteger tablesAvailable[],
                        NSInteger nextTableBySession[],
                        NSInteger *vegetarianCount,
                        NSInteger *veganCount) {
    printf("\nMAKE A BOOKING\n");
    printf("----------------------------------------\n");

    NSInteger sessionIndex = SelectSession(sessionNames);
    if (tablesAvailable[sessionIndex] == 0) {
        printf("Sorry, %s is fully booked.\n", [sessionNames[sessionIndex] UTF8String]);
        return;
    }

    NSString *name = ReadRequiredText(@"Enter passenger name: ", @"Name");
    NSString *cabin = ReadRequiredText(@"Enter cabin number: ", @"Cabin number");
    NSString *diet = SelectDietaryRequirement(dietaryOptions);

    NSInteger tableNumber = nextTableBySession[sessionIndex] + 1;
    Booking *booking = [[Booking alloc] initWithPassengerName:name
                                                  cabinNumber:cabin
                                            dietaryRequirement:diet
                                                   tableNumber:tableNumber];

    bookings[sessionIndex][tableNumber - 1] = booking;
    nextTableBySession[sessionIndex] += 1;
    tablesAvailable[sessionIndex] -= 1;

    if ([diet isEqualToString:@"vegetarian"]) {
        *vegetarianCount += 1;
    } else if ([diet isEqualToString:@"vegan"]) {
        *veganCount += 1;
    }

    printf("\nBooking confirmed!\n");
    printf("Name: %s\n", [booking.passengerName UTF8String]);
    printf("Cabin: %s\n", [booking.cabinNumber UTF8String]);
    printf("Session: %s\n", [sessionNames[sessionIndex] UTF8String]);
    printf("Dietary requirement: %s\n", [booking.dietaryRequirement UTF8String]);
    printf("Table number: %ld\n", (long)booking.tableNumber);
}

static void DisplayDietarySummary(NSInteger vegetarianCount, NSInteger veganCount) {
    printf("\nSPECIAL DIETARY REQUIREMENTS SUMMARY\n");
    printf("----------------------------------------\n");
    printf("Vegetarian: %ld tables\n", (long)vegetarianCount);
    printf("Vegan: %ld tables\n", (long)veganCount);
    printf("Total plant-based: %ld tables\n", (long)(vegetarianCount + veganCount));
}

int main(int argc, const char * argv[]) {
    @autoreleasepool {
        NSArray<NSString *> *sessionNames = @[@"Lunch", @"Early Dinner", @"Late Dinner"];
        NSArray<NSString *> *dietaryOptions = @[@"gluten-free", @"vegetarian", @"vegan", @"diabetic", @"none"];

        NSInteger tablesAvailable[SessionCount] = {TotalTables, TotalTables, TotalTables};
        NSInteger nextTableBySession[SessionCount] = {0, 0, 0};
        NSInteger vegetarianCount = 0;
        NSInteger veganCount = 0;

        NSMutableArray<NSMutableArray<Booking *> *> *bookings = [NSMutableArray arrayWithCapacity:SessionCount];
        for (NSInteger session = 0; session < SessionCount; session++) {
            NSMutableArray<Booking *> *sessionBookings = [NSMutableArray arrayWithCapacity:TotalTables];
            for (NSInteger table = 0; table < TotalTables; table++) {
                [sessionBookings addObject:(Booking *)[NSNull null]];
            }
            [bookings addObject:sessionBookings];
        }

        while (YES) {
            DisplayScreen(sessionNames, tablesAvailable);

            printf("\nMENU:\n");
            printf("1. Make a booking\n");
            printf("2. Display dietary summary\n");
            printf("3. Exit\n");

            NSString *choice = ReadLine(@"Enter your choice (1-3): ");

            if ([choice isEqualToString:@"1"]) {
                MakeBooking(sessionNames,
                            dietaryOptions,
                            bookings,
                            tablesAvailable,
                            nextTableBySession,
                            &vegetarianCount,
                            &veganCount);
            } else if ([choice isEqualToString:@"2"]) {
                DisplayDietarySummary(vegetarianCount, veganCount);
            } else if ([choice isEqualToString:@"3"]) {
                printf("Thank you for using the booking system. Goodbye!\n");
                break;
            } else {
                printf("Invalid choice. Please try again.\n");
            }

            ReadLine(@"\nPress Enter to continue...");
        }
    }
    return 0;
}
