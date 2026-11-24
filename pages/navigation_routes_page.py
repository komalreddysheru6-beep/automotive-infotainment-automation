
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class NavigationRoutesPage:

    ROUTES = (
        By.XPATH,
        '//*[starts-with(@content-desc, "Selected route") '
        'or starts-with(@content-desc, "Alternate route")]'
    )

    SELECTED_ROUTE = (
        By.XPATH,
        '//*[starts-with(@content-desc, "Selected route")]'
    )

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)

    def get_available_routes(self):

        elements = self.driver.find_elements(*self.ROUTES)

        routes = []

        for element in elements:

            description = element.get_attribute(
                "content-desc"
            ) or ""

            if element.is_displayed() and description:

                routes.append({
                    "description": description,
                    "selected": description.startswith(
                        "Selected route"
                    ),
                    "element": element
                })

        return routes

    def get_selected_route(self):

        elements = self.driver.find_elements(
            *self.SELECTED_ROUTE
        )

        for element in elements:

            if element.is_displayed():
                return element.get_attribute("content-desc")

        return None

    def route_identity(self, description):

        for prefix in ("Selected route", "Alternate route"):

            if description.startswith(prefix):
                return description[len(prefix):].strip()

        return description.strip()

    def select_route(self, route):

        expected = self.route_identity(
            route["description"]
        )

        if not route["selected"]:

            rect = route["element"].rect

            self.driver.execute_script(
                "mobile: clickGesture",
                {
                    "x": int(rect["x"] + rect["width"] / 2),
                    "y": int(rect["y"] + rect["height"] / 2)
                }
            )

        def verify_selection(driver):

            selected = self.get_selected_route()

            if selected and self.route_identity(
                selected
            ) == expected:
                return selected

            return False

        return self.wait.until(
            verify_selection,
            message="Requested route selection not verified"
        )

    def choose_route(self):

        routes = self.get_available_routes()

        if not routes:
            print("No accessible route suggestions found.")
            return None

        print("\n========== AVAILABLE ROUTES ==========")

        for index, route in enumerate(routes, 1):

            print(f"{index}. {route['description']}")

        if len(routes) == 1:

            print("\nOnly one accessible route found.")
            choice = 1

        else:

            while True:

                value = input(
                    "\nEnter preferred route number: "
                ).strip()

                if value.isdigit():

                    choice = int(value)

                    if 1 <= choice <= len(routes):
                        break

                print("Invalid route number. Try again.")

        requested_route = routes[choice - 1]

        print("\nRequested route:")
        print(requested_route["description"])

        selected_route = self.select_route(requested_route)

        print("\nVerified selected route:")
        print(selected_route)

        print("Route selection: PASSED")

        return selected_route
