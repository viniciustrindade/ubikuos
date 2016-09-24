package br.edu.ifba.gsort.ubikous;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.wifi.SupplicantState;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import android.preference.PreferenceManager;
import android.speech.RecognitionListener;
import android.speech.RecognizerIntent;
import android.speech.SpeechRecognizer;
import android.speech.tts.TextToSpeech;
import android.support.annotation.UiThread;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.support.v7.widget.Toolbar;
import android.util.Log;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.ImageButton;
import android.widget.TextView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Locale;
import java.util.Map;
import java.util.Random;

public class Speach extends AppCompatActivity {

    final Locale myLocale = new Locale("pt","pt");
    private static final String TAG = "Speach";
    private TextView txtSpeechInput;
    private ImageButton btnSpeak;
    private TextView fala;
    private final int REQ_CODE_SPEECH_INPUT = 100;
    Map<String, Integer> dictionary;
    private static final int EXIT = 1;
    public SpeechRecognizer sr;
    private TextToSpeech tts;
    private RequestQueue queue;
    private String ssid;
    private WifiManager wifiManager;
    private String servidor_ip;
    private String servidor_porta;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        queue = Volley.newRequestQueue(this);

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_speach);
        txtSpeechInput = (TextView) findViewById(R.id.txtSpeechInput);
        btnSpeak = (ImageButton) findViewById(R.id.btnSpeak);
        fala = (TextView) findViewById(R.id.fala);



        tts = new TextToSpeech(getApplicationContext(), new speachListener());

        // hide the action bar
        //  getActionBar().hide();
        populateDictionary();
        sr = SpeechRecognizer.createSpeechRecognizer(this);


        btnSpeak.setOnClickListener(new View.OnClickListener() {

            @Override
            public void onClick(View v) {
                promptSpeechInput();
            }
        });

        wifiManager = (WifiManager) getSystemService(Context.WIFI_SERVICE);

    }
    private void questione(){
        String utteranceId=this.hashCode() + "";
        String[] falas= {"Toque na tela!", "O que deseja?","Se for para ligar a luz, diga liga", "O que posso fazer por você?", "Você é quem manda","O que tem pra hoje?","Se tiver triste, diga a senha!", "Como posso relizá-lo?"};
        Random r = new Random();
        String falaAtual = falas[r.nextInt(10) % falas.length];
        fala.setText(falaAtual);
        tts.speak(falaAtual, TextToSpeech.QUEUE_FLUSH, null,utteranceId);
    }

    @Override
    protected void onStart() {
        super.onStart();
        questione();
        SharedPreferences SP = PreferenceManager.getDefaultSharedPreferences(getBaseContext());

        servidor_ip = SP.getString("pref_key_servidor_ip", "192.168.0.100");
        servidor_porta = SP.getString("pref_key_servidor_porta", "8080");

        if (servidor_ip == null || servidor_porta == null){
            Toast.makeText(this,"IP ou Porta do Servidor não definido", Toast.LENGTH_SHORT);
            return;
        }

        Log.d(TAG,"ip:" + servidor_ip);
        Log.d(TAG,"porta:" + servidor_porta);

    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            Intent settings = new Intent(this,SettingsActivity.class);
            startActivity(settings);

            return true;
        }

        return super.onOptionsItemSelected(item);
    }


    /**
     * Showing google speech input dialog
     * */
    private void promptSpeechInput() {
        Intent intent = new Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH);
        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                RecognizerIntent.LANGUAGE_MODEL_FREE_FORM);

        intent.putExtra(RecognizerIntent.EXTRA_LANGUAGE, myLocale);
        intent.putExtra(RecognizerIntent.EXTRA_PROMPT,
                getString(R.string.speech_prompt));
        try {
            startActivityForResult(intent, REQ_CODE_SPEECH_INPUT);
        } catch (ActivityNotFoundException a) {
            Toast.makeText(getApplicationContext(),
                    getString(R.string.speech_not_supported),
                    Toast.LENGTH_SHORT).show();
        }
    }


    /**
     * Receiving speech input
     * */
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        super.onActivityResult(requestCode, resultCode, data);

        if (servidor_ip == null || servidor_porta == null){
            Toast.makeText(this,"IP ou Porta do Servidor não definido", Toast.LENGTH_SHORT);
            return;
        }

        Log.d(TAG,"ip:" + servidor_ip);
        Log.d(TAG,"porta:" + servidor_porta);
        Log.d(TAG,"porta:" + servidor_porta);


        WifiInfo wifiInfo = wifiManager.getConnectionInfo();
        if (wifiInfo.getSupplicantState() == SupplicantState.COMPLETED) {
            ssid = wifiInfo.getSSID();
        }

        switch (requestCode) {
            case REQ_CODE_SPEECH_INPUT: {
                if (resultCode == RESULT_OK && null != data) {

                    ArrayList<String> result = data
                            .getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS);


                    txtSpeechInput.setText(result.get(0));

                   if (result.size() > 1){
                        String sentence = result.get(0).toLowerCase(myLocale).trim();
                        // Request a string response from the provided URL.
                        String url = "";
                        try {
                            ssid = URLEncoder.encode(ssid, "UTF-8");
                        } catch (UnsupportedEncodingException e) {
                            e.printStackTrace();
                        }
                       url = "http://"+servidor_ip+":"+servidor_porta+"/msg-to-arduino?ssid="+ssid+"&command="+sentence;
                       Log.d(TAG,url);
                       Log.d(TAG,myLocale.getCountry());
                       Log.d(TAG,myLocale.getLanguage());
                        StringRequest stringRequest = new StringRequest(Request.Method.GET, url,
                                new Response.Listener<String>() {
                                    @Override
                                    public void onResponse(String response) {
                                        if (response!=null) {
                                            Log.d(TAG, response + "");
                                            txtSpeechInput.setText(response);
                                            String utteranceId=this.hashCode() + "";
                                            tts.speak(response, TextToSpeech.QUEUE_FLUSH, null,utteranceId);
                                        }

                                    }
                                }, new Response.ErrorListener() {
                            @Override
                            public void onErrorResponse(VolleyError error) {
                                if(error.getMessage()!=null) {
                                    Log.d(TAG, error.getMessage());
                                }
                                   tts.speak("Comando não encontrado", TextToSpeech.QUEUE_FLUSH, null);
                            }
                        });

                        queue.add(stringRequest);



                        Integer operation = dictionary.get(sentence);
                        if(operation != null){
                            switch(operation){
                                case EXIT:{
                                    Speach.this.finish();
                                };break;
                            }
                        }
                    }


                }
                break;
            }

        }
    }


    class speachListener implements TextToSpeech.OnInitListener{


        @Override
        public void onInit(int status) {

            if (status == TextToSpeech.SUCCESS) {
                int result = tts.setLanguage(myLocale);

                if (result == TextToSpeech.LANG_MISSING_DATA
                        || result == TextToSpeech.LANG_NOT_SUPPORTED) {
                    Log.e("TTS", "This Language is not supported");
                    Intent installIntent = new Intent();
                    installIntent.setAction(TextToSpeech.Engine.ACTION_INSTALL_TTS_DATA);
                    startActivity(installIntent);
                } else {
                    btnSpeak.setEnabled(true);

                }

            } else {
                Log.e("TTS", "Initilization Failed!");
            }

        }
    }

    @Override
    public void onDestroy() {
        // Don't forget to shutdown tts!
        if (tts != null) {
            tts.stop();
            tts.shutdown();
        }
        super.onDestroy();
    }



    private void populateDictionary() {
        dictionary = new HashMap<String, Integer>();
        dictionary.put("exit", EXIT);
        dictionary.put("close", EXIT);
    }


    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }
}
