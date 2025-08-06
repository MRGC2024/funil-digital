from datetime import datetime
from src.models import db

class TrackingPixel(db.Model):
    """Modelo para pixels de tracking"""
    
    __tablename__ = 'tracking_pixels'
    
    id = db.Column(db.Integer, primary_key=True)
    funnel_id = db.Column(db.Integer, db.ForeignKey('funnels.id'), nullable=False)
    step_id = db.Column(db.Integer, db.ForeignKey('funnel_steps.id'), nullable=True)  # Null = aplicar a todo o funil
    pixel_type = db.Column(db.String(50), nullable=False)  # 'facebook', 'google', 'tiktok', 'custom'
    pixel_id = db.Column(db.String(255), nullable=False)
    event_name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        """Converte o modelo para dicionário"""
        return {
            'id': self.id,
            'funnel_id': self.funnel_id,
            'step_id': self.step_id,
            'pixel_type': self.pixel_type,
            'pixel_id': self.pixel_id,
            'event_name': self.event_name,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def clone(self, new_funnel_id, new_step_id=None):
        """Clona o pixel para um novo funil"""
        new_pixel = TrackingPixel(
            funnel_id=new_funnel_id,
            step_id=new_step_id or self.step_id,
            pixel_type=self.pixel_type,
            pixel_id=self.pixel_id,
            event_name=self.event_name,
            is_active=self.is_active
        )
        return new_pixel
    
    def generate_script(self):
        """Gera o script do pixel baseado no tipo"""
        if self.pixel_type == 'facebook':
            return self._generate_facebook_pixel()
        elif self.pixel_type == 'google':
            return self._generate_google_pixel()
        elif self.pixel_type == 'tiktok':
            return self._generate_tiktok_pixel()
        else:
            return self._generate_custom_pixel()
    
    def _generate_facebook_pixel(self):
        """Gera script do Facebook Pixel"""
        script = """
        <!-- Facebook Pixel Code -->
        <script>
        !function(f,b,e,v,n,t,s)
        {if(f.fbq)return;n=f.fbq=function(){n.callMethod?
        n.callMethod.apply(n,arguments):n.queue.push(arguments)};
        if(!f._fbq)f._fbq=n;n.push=n;n.loaded=!0;n.version='2.0';
        n.queue=[];t=b.createElement(e);t.async=!0;
        t.src=v;s=b.getElementsByTagName(e)[0];
        s.parentNode.insertBefore(t,s)}(window, document,'script',
        'https://connect.facebook.net/en_US/fbevents.js');
        fbq('init', '""" + self.pixel_id + """');
        fbq('track', 'PageView');
        """
        
        if self.event_name:
            script += "fbq('track', '" + self.event_name + "');"
        
        script += """
        </script>
        <noscript><img height="1" width="1" style="display:none"
        src="https://www.facebook.com/tr?id=""" + self.pixel_id + """&ev=PageView&noscript=1"
        /></noscript>
        <!-- End Facebook Pixel Code -->
        """
        
        return script
    
    def _generate_google_pixel(self):
        """Gera script do Google Analytics/Ads"""
        script = """
        <!-- Google tag (gtag.js) -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=""" + self.pixel_id + """"></script>
        <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', '""" + self.pixel_id + """');
        """
        
        if self.event_name:
            script += "gtag('event', '" + self.event_name + "');"
        
        script += """
        </script>
        """
        
        return script
    
    def _generate_tiktok_pixel(self):
        """Gera script do TikTok Pixel"""
        script = """
        <!-- TikTok Pixel Code -->
        <script>
        !function (w, d, t) {
        w.TiktokAnalyticsObject=t;var ttq=w[t]=w[t]||[];ttq.methods=["page","track","identify","instances","debug","on","off","once","ready","alias","group","enableCookie","disableCookie"],ttq.setAndDefer=function(t,e){t[e]=function(){t.push([e].concat(Array.prototype.slice.call(arguments,0)))}};for(var i=0;i<ttq.methods.length;i++)ttq.setAndDefer(ttq,ttq.methods[i]);ttq.instance=function(t){for(var e=ttq._i[t]||[],n=0;n<ttq.methods.length;n++)ttq.setAndDefer(e,ttq.methods[n]);return e},ttq.load=function(e,n){var i="https://analytics.tiktok.com/i18n/pixel/events.js";ttq._i=ttq._i||{},ttq._i[e]=[],ttq._i[e]._u=i,ttq._t=ttq._t||{},ttq._t[e]=+new Date,ttq._o=ttq._o||{},ttq._o[e]=n||{};var o=document.createElement("script");o.type="text/javascript",o.async=!0,o.src=i+"?sdkid="+e+"&lib="+t;var a=document.getElementsByTagName("script")[0];a.parentNode.insertBefore(o,a)};
        ttq.load('""" + self.pixel_id + """');
        ttq.page();
        """
        
        if self.event_name:
            script += "ttq.track('" + self.event_name + "');"
        
        script += """
        }(window, document, 'ttq');
        </script>
        <!-- End TikTok Pixel Code -->
        """
        
        return script
    
    def _generate_custom_pixel(self):
        """Gera script customizado"""
        script = """
        <!-- Custom Pixel -->
        <script>
        // Custom pixel code for """ + self.pixel_id + """
        console.log('Custom pixel fired: """ + self.pixel_id + """');
        """
        
        if self.event_name:
            script += "console.log('Event: " + self.event_name + "');"
        
        script += """
        </script>
        <!-- End Custom Pixel -->
        """
        
        return script
    
    @staticmethod
    def get_funnel_pixels(funnel_id, step_id=None):
        """Retorna todos os pixels ativos para um funil/etapa"""
        query = TrackingPixel.query.filter_by(funnel_id=funnel_id, is_active=True)
        
        if step_id:
            # Pixels específicos da etapa + pixels globais do funil
            query = query.filter(
                (TrackingPixel.step_id == step_id) | 
                (TrackingPixel.step_id.is_(None))
            )
        else:
            # Apenas pixels globais do funil
            query = query.filter(TrackingPixel.step_id.is_(None))
        
        return query.all()
    
    def __repr__(self):
        return f'<TrackingPixel {self.pixel_type} - {self.pixel_id}>'

