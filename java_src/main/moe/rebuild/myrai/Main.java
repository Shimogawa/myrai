package moe.rebuild.myrai;

import net.mamoe.mirai.Bot;
import net.mamoe.mirai.BotFactory;
import net.mamoe.mirai.contact.Contact;
import net.mamoe.mirai.contact.User;
import net.mamoe.mirai.event.events.BotEvent;
import net.mamoe.mirai.event.events.MessageEvent;
import net.mamoe.mirai.message.data.*;
import py4j.GatewayServer;

public class Main {
    public static void main(String[] args) {
        var gw = new GatewayServer(new Main());
        gw.start();
    }
}
