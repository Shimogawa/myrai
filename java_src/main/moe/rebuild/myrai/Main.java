package moe.rebuild.myrai;

import py4j.GatewayServer;

public class Main {
    public static void main(String[] args) {
        var gw = new GatewayServer(new Main());
        gw.start();
    }
}
