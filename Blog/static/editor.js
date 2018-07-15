var editor = new Simditor({
                  textarea: $('#editor'),
                  placeholder: '欢迎评论，一起探讨，共同进步。编辑器支持MD语法，编辑完成后CMD/Ctrl + M转换为MD格式。',
                  toolbar: ['bold', 'italic', 'underline', 'color', 'fontScale', 'strikethrough', '|', 'blockquote', 'code', '|',
                      'indent', 'outdent', 'alignment', '|', 'ol', 'ul', '|', 'marked','emoji'],
                  toolbarFloat: false,
                  emoji:{
                      imagePath:'../../../static/images/emoji/',
                      images:['smile.png','smiley.png','laughing.png','blush.png','heart_eyes.png','smirk.png','flushed.png',
                          'grin.png','wink.png','kissing_closed_eyes.png','stuck_out_tongue_winking_eye.png',
                          'stuck_out_tongue.png','sleeping.png','worried.png','expressionless.png','sweat_smile.png',
                          'cold_sweat.png','joy.png','sob.png','angry.png','mask.png','scream.png','sunglasses.png',
                          'heart.png','broken_heart.png','star.png','anger.png','exclamation.png','question.png','zzz.png',
                          'thumbsup.png','thumbsdown.png','ok_hand.png','punch.png','v.png','clap.png','muscle.png','pray.png',
                          'skull.png','trollface.png','anger_face.png','awkward.png','Bandage.png','cool.png','cry-smiley.png',
                          'cute.png','Eyes_heart.png','food_savoring.png','grimacing.png','happy.png','joy_of_tears_with.png',
                          'love.png','shut_up.png', 'sleep.png','smiley-face-emoji.png','smiley-face-mouth-emoji.png',
                          'superstruck.png','surprised.png', 'wow.png']
                  }
              });