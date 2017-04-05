package com.company;

import com.mashape.unirest.http.HttpResponse;

import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;

import com.mashape.unirest.http.async.Callback;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.jnativehook.GlobalScreen;
import org.jnativehook.NativeHookException;
import com.google.gson.Gson;

import java.io.InputStream;
import java.util.ArrayList;
import java.util.LinkedHashMap;
import java.util.Map;

import java.util.concurrent.Future;
import java.util.logging.Level;
import java.util.logging.Logger;





public class Main {
    static Map<String, String> releaseQueue = new LinkedHashMap<>();

    static ArrayList keyData = new ArrayList();
    static ArrayList mouseData = new ArrayList();

    static String url = "http://127.0.0.1:5000/test";

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



    public static void triggerRelease(String keyCode, String timestamp) throws UnirestException{
        LinkedHashMap<String, String> keyEventData = new LinkedHashMap<>();
        keyEventData.put("keyPress", releaseQueue.get(keyCode));
        keyEventData.put("keyRelease", timestamp);
        keyEventData.put("keyCode", keyCode);
        keyData.add(keyEventData);



        if (keyData.size() >= 130) {
            Gson gson = new Gson();

            String keyDataJson = gson.toJson(keyData, ArrayList.class);


            Future<HttpResponse<JsonNode>> future = Unirest.post(url)
                    .header("accept", "application/json")
                    .body(keyDataJson)
                    .asJsonAsync(new Callback<JsonNode>() {

                        public void failed(UnirestException e) {

                        }

                        public void completed(HttpResponse<JsonNode> response) {
                            keyData.clear();
                        }

                        public void cancelled() {

                        }

                    });

        }




    }

    static String mouseReleaseQueue = "";

    public void uploadAndClear()

    public static void triggerMousePress(String timestamp){
        mouseReleaseQueue = timestamp;
    }

    public static void triggerMouseRelease(String button, String timestamp){
        LinkedHashMap<String, String> mouseEventData = new LinkedHashMap<>();
        mouseEventData.put("mousePress", mouseReleaseQueue);
        mouseEventData.put("mouseRelease", timestamp);
        mouseEventData.put("buttonCode", button);
        mouseData.add(mouseEventData);


        if (mouseData.size() >= 130) {
            Gson gson = new Gson();

            String keyDataJson = gson.toJson(mouseData, ArrayList.class);


            Future<HttpResponse<JsonNode>> future = Unirest.post(url)
                    .header("accept", "application/json")
                    .body(keyDataJson)
                    .asJsonAsync(new Callback<JsonNode>() {

                        public void failed(UnirestException e) {

                        }

                        public void completed(HttpResponse<JsonNode> response) {
                            mouseData.clear();
                        }

                        public void cancelled() {

                        }

                    });

        }



    }
}
