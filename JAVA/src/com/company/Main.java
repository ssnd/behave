package com.company;

import com.mashape.unirest.http.HttpResponse;

import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;

import com.mashape.unirest.http.async.Callback;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.jnativehook.GlobalScreen;
import org.jnativehook.NativeHookException;
import com.google.gson.Gson;
import org.json.JSONObject;

import javax.swing.*;
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

        if(releaseQueue.get(keyCode) == null){
            return;
        }
        LinkedHashMap<String, String> keyEventData = new LinkedHashMap<>();
        keyEventData.put("keyPress", releaseQueue.get(keyCode));
        keyEventData.put("keyRelease", timestamp);
        keyEventData.put("keyCode", keyCode);
        keyData.add(keyEventData);

        System.out.println(keyEventData);

        if (keyData.size() >= 60) {
            Gson gson = new Gson();

            String keyDataJson = gson.toJson(keyData, ArrayList.class);

            System.out.println("DATA SENDING -- ");


            Future<HttpResponse<JsonNode>> future = Unirest.post("http://127.0.0.1:5000/keyboard")
                    .header("accept", "application/json")
                    .body(keyDataJson)
                    .asJsonAsync(new Callback<JsonNode>() {

                        public void failed(UnirestException e) {
                            System.out.println("FAILED");
                        }

                        public void completed(HttpResponse<JsonNode> response) {

                            JsonNode body = response.getBody();

                            System.out.println(body);

                            JSONObject myObj = response.getBody().getObject();

                            String responseStr = myObj.getString("status");

                            if(responseStr.equals("INTERRUPT")){
                                System.out.println("--INTERRUPTION");
                                JOptionPane.showMessageDialog(null, "Another person is using this pc.");
                            }


                            keyData.clear();
                        }

                        public void cancelled() {
                            System.out.println("CANCELLED");
                        }

                    });

            keyData.clear();

        }




    }

    static String mouseReleaseQueue = "";

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


            Future<HttpResponse<JsonNode>> future = Unirest.post("http://127.0.0.1:5000/mouse")
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
