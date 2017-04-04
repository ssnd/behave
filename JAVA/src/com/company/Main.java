package com.company;

import org.jnativehook.GlobalScreen;
import org.jnativehook.NativeHookException;
import com.google.gson.Gson;
import com.google.gson.GsonBuilder;

import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.logging.Level;
import java.util.logging.Logger;

public class Main {
    static Map<String, String> releaseQueue = new LinkedHashMap<>();

    static ArrayList keyData = new ArrayList();
    static ArrayList mouseData = new ArrayList();

    public static void main(String[] args) {

        Logger logger = Logger.getLogger(GlobalScreen.class.getPackage().getName());
        logger.setLevel(Level.OFF);

        System.out.println("Initialized");

        try {
            GlobalScreen.registerNativeHook();
        }
        catch (NativeHookException ex) {
            System.err.println("There was a problem registering the native hook.");
            System.err.println(ex.getMessage());

            System.exit(1);
        }

        GlobalScreen.addNativeKeyListener(new KeyListener());

        MouseListener mouseListenerObject = new MouseListener();

        GlobalScreen.addNativeMouseListener(mouseListenerObject);
        GlobalScreen.addNativeMouseMotionListener(mouseListenerObject);
    }

    public static void triggerPress(String keyCode, String timestamp){
        releaseQueue.put(keyCode, timestamp);
    }

    public static void triggerRelease(String keyCode, String timestamp){
        Map<String, String> keyEventData = new LinkedHashMap<>();
        keyEventData.put("keyPress", releaseQueue.get(keyCode));
        keyEventData.put("keyRelease", timestamp);
        keyEventData.put("keyCode", keyCode);
        keyData.add(keyEventData);

        System.out.println(keyEventData);

    }

    static String mouseReleaseQueue = "";

    public static void triggerMousePress(String timestamp){
        mouseReleaseQueue = timestamp;
    }

    public static void triggerMouseRelease(String button, String timestamp){
        Map<String, String> mouseEventData = new LinkedHashMap<>();
        mouseEventData.put("mousePress", mouseReleaseQueue);
        mouseEventData.put("mouseRelease", timestamp);
        mouseEventData.put("buttonCode", button);
        mouseData.add(mouseEventData);

        System.out.println(mouseEventData);
    }
}
