#include <SFML/Graphics.hpp>
#include <iostream>
#include <fstream>
#include <bitset>
using namespace std;

int bitify() {
        std::ifstream infile("file.5bf");
        while (infile) {

            //initialize variables

            char c;
            infile.get(c);
            for (int i = 0; i < 5; ++i) { //read 5 times
                int ac = (int)c; //converts byte to integer

                infile.get(c); //read new byte
            }


        }
        return 0;
}


int main()
{
    sf::RenderWindow window(sf::VideoMode(200, 200), "SFML works!");
    sf::CircleShape shape(100.f);
    sf::Font font;
    if (!font.loadFromFile("5bitfont.ttf"))
    {
        window.close();
    }
    sf::Text text; //loading stuff
    shape.setFillColor(sf::Color::Green);
    text.setFont(font);
    text.setString("abcdefghijklmnopqrs\ntuvwxyzabcdefghijklmnopqrstuvwxyz"); //setting object properties
    bitify();
    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
                window.close(); //closes window if x is pressed
        }

        window.clear();
        window.draw(shape); //draws to screen
        window.draw(text);
        window.display();
    }

    return 0;
}