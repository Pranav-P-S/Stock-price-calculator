use eframe::egui;

fn main() -> eframe::Result<()> {
    env_logger::init(); // Log to stderr (if you run with `RUST_LOG=debug`).
    let options = eframe::NativeOptions {
        viewport: egui::ViewportBuilder::default().with_inner_size([600.0, 950.0]),
        ..Default::default()
    };
    eframe::run_native(
        "Stock Price Calculation",
        options,
        Box::new(|_cc| Ok(Box::new(StockApp::default()))),
    )
}

struct StockApp {
    // Input strings
    current_price: String,
    num_shares: String,
    desired_profit_percentage: String,
    desired_loss_percentage: String,
    brokerage_constant: String,
    brokerage_percentage: String,

    // Outputs
    total_invested: f64,
    profit_price: f64,
    total_profit: f64,
    loss_price: f64,
    total_loss: f64,
    
    // Output label colors/state
    calculation_done: bool,
    error_message: Option<String>,
}

impl Default for StockApp {
    fn default() -> Self {
        Self {
            current_price: "".to_owned(),
            num_shares: "".to_owned(),
            desired_profit_percentage: "".to_owned(),
            desired_loss_percentage: "".to_owned(),
            brokerage_constant: "".to_owned(),
            brokerage_percentage: "".to_owned(),
            
            total_invested: 0.0,
            profit_price: 0.0,
            total_profit: 0.0,
            loss_price: 0.0,
            total_loss: 0.0,
            calculation_done: false,
            error_message: None,
        }
    }
}

impl eframe::App for StockApp {
    fn update(&mut self, ctx: &egui::Context, _frame: &mut eframe::Frame) {
        egui::CentralPanel::default().show(ctx, |ui| {
            // Set dark theme style explicitly if needed, but egui defaults are usually good.
            // We can add some padding/spacing to match the "clean" look.
            
            let scroll = egui::ScrollArea::vertical();
            scroll.show(ui, |ui| {
                ui.vertical_centered(|ui| {
                    ui.heading("Stock Price Calculation");
                });
                ui.add_space(20.0);

                // Helper for inputs
                let input_field = |ui: &mut egui::Ui, label: &str, value: &mut String| {
                    ui.horizontal(|ui| {
                        ui.label(egui::RichText::new(label).strong().size(14.0));
                        ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                            ui.add(egui::TextEdit::singleline(value).desired_width(200.0));
                        });
                    });
                    ui.add_space(10.0);
                };

                ui.group(|ui| {
                    input_field(ui, "Current Stock Price ($):", &mut self.current_price);
                    input_field(ui, "Number of Shares:", &mut self.num_shares);
                    input_field(ui, "Desired Profit (%):", &mut self.desired_profit_percentage);
                    input_field(ui, "Desired Loss (%):", &mut self.desired_loss_percentage);
                    input_field(ui, "Brokerage Constant ($):", &mut self.brokerage_constant);
                    input_field(ui, "Brokerage Percentage (%):", &mut self.brokerage_percentage);
                });

                ui.add_space(20.0);

                // Calculate Button
                ui.vertical_centered(|ui| {
                    if ui.add(egui::Button::new(egui::RichText::new("Calculate").size(16.0).strong()).min_size(egui::vec2(200.0, 40.0))).clicked() {
                        self.calculate();
                    }
                });

                ui.add_space(20.0);

                // Outputs
                // Clean rounded font style logic is handled by egui's defaults mostly, 
                // but we can adjust size.
                
                if let Some(err) = &self.error_message {
                    ui.vertical_centered(|ui| {
                        ui.colored_label(egui::Color32::RED, egui::RichText::new(format!("Input Error: {}", err)).size(16.0));
                    });
                } 
                
                if self.calculation_done {
                    // Frame for outputs
                    egui::Frame::group(ui.style()).show(ui, |ui| {
                        let output_row = |ui: &mut egui::Ui, label: &str, value: String, color: egui::Color32| {
                            ui.horizontal(|ui| {
                                ui.label(egui::RichText::new(label).size(14.0));
                                ui.with_layout(egui::Layout::right_to_left(egui::Align::Center), |ui| {
                                    ui.label(egui::RichText::new(value).color(color).size(14.0).strong());
                                });
                            });
                            ui.add_space(5.0);
                        };

                        output_row(ui, "Total Investment:", format!("${:.2}", self.total_invested), egui::Color32::WHITE);
                        output_row(ui, "Price per share to sell for profit:", format!("${:.2}", self.profit_price), egui::Color32::GREEN);
                        output_row(ui, "Total Profit:", format!("${:.2}", self.total_profit), egui::Color32::GREEN);
                        output_row(ui, "Price per share to sell for loss:", format!("${:.2}", self.loss_price), egui::Color32::RED);
                        output_row(ui, "Total Loss:", format!("${:.2}", self.total_loss), egui::Color32::RED);
                    });
                }
            });
        });
    }
}

impl StockApp {
    fn calculate(&mut self) {
        // Helper to parse
        let parse = |s: &str, name: &str| -> Result<f64, String> {
            s.trim().parse::<f64>().map_err(|_| format!("Invalid numeric value for {}", name))
        };

        let current_price = match parse(&self.current_price, "Current Price") { Ok(v) => v, Err(e) => { self.error(&e); return; }};
        let num_shares = match parse(&self.num_shares, "Number of Shares") { Ok(v) => v, Err(e) => { self.error(&e); return; }};
        let desired_profit_percentage = match parse(&self.desired_profit_percentage, "Profit %") { Ok(v) => v, Err(e) => { self.error(&e); return; }};
        let desired_loss_percentage = match parse(&self.desired_loss_percentage, "Loss %") { Ok(v) => v, Err(e) => { self.error(&e); return; }};
        let brokerage_constant = match parse(&self.brokerage_constant, "Brokerage Constant") { Ok(v) => v, Err(e) => { self.error(&e); return; }};
        let brokerage_percentage = match parse(&self.brokerage_percentage, "Brokerage Percentage") { Ok(v) => v, Err(e) => { self.error(&e); return; }};

        if brokerage_percentage < 0.0 {
            self.error("Brokerage percentage cannot be negative");
            return;
        }

        self.error_message = None;

        // Logic Port
        self.total_invested = current_price * num_shares;

        let initial_brokerage = if brokerage_percentage != 0.0 {
            let threshold = (brokerage_constant * 100.0) / brokerage_percentage;
            if current_price > threshold {
                 brokerage_constant
            } else {
                 (brokerage_percentage * current_price) / 100.0
            }
        } else {
            // Division by zero risk in threshold calc if percentage is 0. 
            // In python code: threshold = (constant * 100) / percentage. 
            // If percentage is 0, this crashes Python unless caught.
            // Assuming 0% brokerage implies 0 variable cost.
            // But if constant logic applies... if brok_pct is 0, threshold is Inf. 
            // current_price > Inf is False. 
            // so else: (0 * price)/100 = 0.
            0.0
        };

        let denominator = 100.0 - brokerage_percentage;
        if denominator == 0.0 {
             self.error("Brokerage percentage cannot be 100%");
             return;
        }

        let sell_profit_p = ((100.0 + desired_profit_percentage) / denominator) * current_price 
                          + ((100.0 * initial_brokerage) / denominator);
        
        let sell_profit_c = ((100.0 + desired_profit_percentage) / 100.0) * current_price 
                          + initial_brokerage + brokerage_constant;

        let sell_loss_p = ((100.0 - desired_loss_percentage) / denominator) * current_price 
                        + ((100.0 * initial_brokerage) / denominator);
        
        let sell_loss_c = ((100.0 - desired_loss_percentage) / 100.0) * current_price 
                        + initial_brokerage + brokerage_constant;

        let profit_brokerage;
        if sell_profit_p > sell_profit_c {
            profit_brokerage = brokerage_constant;
            self.profit_price = sell_profit_c;
        } else {
            profit_brokerage = (brokerage_percentage / 100.0) * sell_profit_p;
            self.profit_price = sell_profit_p;
        }

        let loss_brokerage;
        if sell_loss_p > sell_loss_c {
            loss_brokerage = brokerage_constant;
            self.loss_price = sell_loss_c;
        } else {
            loss_brokerage = (brokerage_percentage / 100.0) * sell_loss_p;
            self.loss_price = sell_loss_p;
        }

        let profit_per_share = self.profit_price - current_price - initial_brokerage - profit_brokerage;
        self.total_profit = num_shares * profit_per_share;

        let loss_per_share = self.loss_price - current_price - initial_brokerage - loss_brokerage;
        self.total_loss = num_shares * loss_per_share;

        self.calculation_done = true;
    }

    fn error(&mut self, msg: &str) {
        self.error_message = Some(msg.to_owned());
        self.calculation_done = false;
    }
}
