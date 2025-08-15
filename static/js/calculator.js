
    Vue.component("calculator", {
      props: {
        auctionsProps: Object,
        calculatorVarsProps: Object,
        platformsProps: Array,
        pricesProps: Array,
        bidFeeProps: Array,
        buyerFeeProps: Array,
        portsProps: Array,
        seaDeliveryProps: Array,
        carTypesProps: Array,
        fuelTypesProps: Array,
        containerImages: Object,
        auctionsPricesProps: Array,
      },
      data: function () {
        return {
          auctions: {},
          calculatorVars: [],
          prices: [],
          bidFee: [],
          buyerFee: [],
          seaDelivery: [],
          carTypes: [],
          carLink: "",
          price: "",
          auctionId: 0,
          carType: "",
          platformId: 0,
          portId: 0,
          fuelId: 0,
          volumeEngine: "",
          carYear: 0,
          isSublot: !1,
        };
      },
      mounted: function () {
        this.initData();
      },
      methods: {
        initData: function () {
          (this.auctions = this.auctionsProps),
            (this.calculatorVars = this.calculatorVarsProps),
            (this.prices = this.pricesProps),
            (this.bidFee = this.bidFeeProps),
            (this.buyerFee = this.buyerFeeProps),
            (this.seaDelivery = this.seaDeliveryProps),
            (this.carTypes = this.carTypesProps);
        },
        changeAuction: function (e) {
          (this.auctionId = parseInt(e)),
            (this.portId = 0),
            (this.platformId = 0);
        },
        changeCarType: function (e) {
          this.carType = e;
        },
        changePlatform: function () {
          this.portId = 0;
        },
        checkCalc: function () {
          return Boolean(
            this.auctionId &&
              parseFloat(this.price) > 0 &&
              this.auctionId > 0 &&
              this.platformId > 0 &&
              this.portId > 0 &&
              this.fuelId > 0 &&
              this.volumeEngine > 0 &&
              "" !== this.carType &&
              this.carYear > 0
          );
        },
        checkAuctionPrice: function () {
          return Boolean(this.price > 0 && this.auctionId > 0);
        },
        checkPortDelivery: function () {
          return Boolean(
            "" !== this.carType && this.platformId > 0 && this.portId > 0
          );
        },
        checkSeaDeliveryPrice: function () {
          return Boolean(this.portId > 0 && "" !== this.carType);
        },
        checkExciseTax: function () {
          return Boolean(this.volumeEngine > 0 && this.carYear > 0);
        },
        checkDuty: function () {
          return Boolean(
            (this.price > 0 &&
              this.checkAuctionPrice() &&
              "" !== this.carType) ||
              3 === this.fuelId
          );
        },
        checkVat: function () {
          return Boolean(
            (this.checkDuty &&
              this.checkExciseTax &&
              this.price > 0 &&
              "" !== this.carType &&
              this.checkAuctionPrice()) ||
              3 === this.fuelId
          );
        },
        checkBroker: function () {
          return this.price > 0;
        },
        checkExpedit: function () {
          return this.price > 0;
        },
        checkKyivDelivery: function () {
          return this.price > 0;
        },
        checkCert: function () {
          return this.price > 0;
        },
        checkRegister: function () {
          return Boolean(
            this.price > 0 && "" !== this.carType && this.checkAuctionPrice()
          );
        },
        checkServices: function () {
          return this.price > 0;
        },
        getAdditionalAuctionPrice: function () {
          for (var e in this.auctionsPricesProps) {
            if (
              this.auctionsPricesProps[e].auction_id === this.auctionId &&
              this.price >=
                parseFloat(this.auctionsPricesProps[e].price_from) &&
              this.price <= parseFloat(this.auctionsPricesProps[e].price_to)
            )
              return parseFloat(this.auctionsPricesProps[e].amount) > 0
                ? parseFloat(this.auctionsPricesProps[e].amount)
                : (parseFloat(this.auctionsPricesProps[e].percent) / 100) *
                    this.price;
          }
          return 0;
        },
      },
      computed: {
        fuelTypes: function () {
          return "moto" === this.carType
            ? ((this.fuelId = 2),
              this.fuelTypesProps.filter(function (e) {
                return "Р‘РµРЅР·РёРЅ" === e.name;
              }))
            : this.fuelTypesProps;
        },
        colorPortCa: function () {
          return "CA Los Angeles" === this.selectedPortName
            ? "black"
            : "#0988ff";
        },
        colorPortFl: function () {
          return "FL Maiami" === this.selectedPortName ? "black" : "#0988ff";
        },
        colorPortTx: function () {
          return "TX Houston" === this.selectedPortName ? "black" : "#0988ff";
        },
        colorPortNj: function () {
          return "NJ Newark" === this.selectedPortName ? "black" : "#0988ff";
        },
        colorPortGa: function () {
          return "GA Savannah" === this.selectedPortName ? "black" : "#0988ff";
        },
        portDelivery: function () {
          var e = this,
            t = this.prices.filter(function (t) {
              return t.platform_id === e.platformId && t.port_id === e.portId;
            });
          return void 0 !== t[0]
            ? Math.round(
                parseFloat(t[0][this.carType]) +
                  ("mediumtruck" === this.carType
                    ? 0.5 * parseFloat(t[0][this.carType])
                    : 0)
              ) + 150
            : 0;
        },
        dangerCargo: function () {
          var e = +this.calculatorVarsProps.dangerCargo.val;
          return 3 === this.fuelId || 4 === this.fuelId ? e : 0;
        },
        getAuctionPrice: function () {
          var e = 0,
            t = 0,
            n = 0;
          if (this.price > 0 && this.auctionId > 0) {
            for (var r in this.bidFee)
              if (
                parseFloat(this.price) >=
                  parseFloat(this.bidFee[r].begin_price) &&
                parseFloat(this.price) <=
                  parseFloat(this.bidFee[r].end_price) &&
                parseInt(this.bidFee[r].auction_id) === this.auctionId
              ) {
                e = parseFloat(this.bidFee[r].bid_fee);
                break;
              }
            for (var a in this.buyerFee)
              parseFloat(this.price) >=
                parseFloat(this.buyerFee[a].begin_price) &&
                parseFloat(this.price) <=
                  parseFloat(this.buyerFee[a].end_price) &&
                parseInt(this.buyerFee[a].auction_id) === this.auctionId &&
                ((t = this.buyerFee[a].fee_percent),
                (n = parseFloat(this.buyerFee[a].buyer_fee)));
            return (
              this.getAdditionalAuctionPrice() +
              e +
              parseFloat(this.auctions[this.auctionId].gate_fee) +
              parseFloat(this.auctions[this.auctionId].storage_fee) +
              parseFloat(this.price) * t +
              n
            );
          }
          return 0;
        },
        platforms: function () {
          var e = this;
          return this.platformsProps.filter(function (t) {
            return t.auction_id === e.auctionId;
          });
        },
        stateCode: function () {
          var e = this,
            t = this.platformsProps.filter(function (t) {
              return t.id === e.platformId;
            });
          return void 0 !== t[0] ? t[0].state_code : "";
        },
        containerImage: function () {
          return void 0 !== this.containerImages[this.carType]
            ? this.containerImages[this.carType]
            : "";
        },
        ports: function () {
          var e = this;
          return this.portsProps.filter(function (t) {
            return t.platform_id === e.platformId;
          });
        },
        seaDeliveryPrice: function () {
          var e = this,
            t = this.seaDelivery.filter(function (t) {
              return t.port_id === e.portId;
            });
          return void 0 !== t[0] ? parseFloat(t[0][this.carType]) + 100 : 0;
        },
        selectedPortName: function () {
          var e = this,
            t = this.portsProps.filter(function (t) {
              return t.id === e.portId;
            });
          return void 0 !== t[0] ? t[0].name : "";
        },
        broker: function () {
          return "moto" === this.carType
            ? parseFloat(this.calculatorVarsProps.brokerMoto.val)
            : parseFloat(this.calculatorVarsProps.broker.val) + 70;
        },
        expedit: function () {
          return "moto" === this.carType
            ? parseFloat(this.calculatorVarsProps.expeditMoto.val)
            : "mediumtruck" === this.carType
            ? parseFloat(this.calculatorVarsProps.expeditTruck.val)
            : parseFloat(this.calculatorVarsProps.expedit.val);
        },
        sublotPrice: function () {
          return this.isSublot
            ? parseFloat(this.calculatorVarsProps.sublot.val)
            : 0;
        },
        cert: function () {
          switch (this.carType) {
            case "moto":
              return parseFloat(this.calculatorVarsProps.certificationMoto.val);
            default:
              return parseFloat(this.calculatorVarsProps.certification.val);
          }
        },
        kyivDelivery: function () {
          return "moto" === this.carType
            ? parseFloat(this.calculatorVarsProps.motoDelivery.val)
            : ["minivan", "miniven", "heavy"].includes(this.carType)
            ? parseFloat(this.calculatorVarsProps.heavyMinivanDelivery.val)
            : ["mediumtruck"].includes(this.carType)
            ? parseFloat(this.calculatorVarsProps.mediumtruckDelivery.val)
            : parseFloat(this.calculatorVarsProps.kyivDelivery.val);
        },
        services: function () {
          return parseFloat(this.calculatorVarsProps.services.val) + 100;
        },
        register: function () {
          if (3 === this.fuelId)
            return Math.round(
              parseFloat(this.calculatorVarsProps.register_price_electro.val) /
                parseFloat(this.calculatorVarsProps.currencyDoll.val)
            );
          if ("moto" === this.carType)
            return Math.round(
              parseFloat(this.calculatorVarsProps.register_price_moto.val) /
                parseFloat(this.calculatorVarsProps.currencyDoll.val)
            );
          for (
            var e = parseFloat(this.calculatorVarsProps.register_koef.val),
              t = this.calculatorVarsProps.register_koef.conditional_data,
              n =
                parseFloat(this.price) +
                this.customsPrice +
                this.getAuctionPrice,
              r = 0;
            r < t.length;
            r++
          )
            n >= +t[r].from_condition &&
              n <= +t[r].to_condition &&
              (e = parseFloat(t[r].value));
          return Math.round(
            n * e +
              parseFloat(this.calculatorVarsProps.register_price.val) /
                parseFloat(this.calculatorVarsProps.currencyDoll.val)
          );
        },
        insurance: function () {
          var e =
              "moto" === this.carType
                ? parseFloat(this.calculatorVarsProps.insuranceMoto.val)
                : parseFloat(this.calculatorVarsProps.insurance.val),
            t = Math.round((parseFloat(this.price) + this.getAuctionPrice) * e);
          return t >= 50 ? t : t > 0 ? 50 : 0;
        },
        vat: function () {
          return 3 === this.fuelId
            ? 0
            : Math.round(
                (this.duty +
                  this.exciseTax +
                  (parseFloat(this.price) +
                    this.customsPrice +
                    this.getAuctionPrice)) *
                  parseFloat(this.calculatorVarsProps.vat.val)
              );
        },
        customsSumm: function () {
          return Math.round(this.exciseTax + this.duty + this.vat);
        },
        customsPrice: function () {
          var e = 0;
          switch (this.carType) {
            case "moto":
              e = parseFloat(this.calculatorVarsProps.customsPriceMoto.val);
              break;
            case "p3cars":
              e = parseFloat(this.calculatorVarsProps.customsPriceSedan.val);
              break;
            case "p2cars":
              e = parseFloat(this.calculatorVarsProps.customsPriceSuv.val);
              break;
            case "mediumtruck":
              e = parseFloat(this.calculatorVarsProps.customsPricePickup.val);
              break;
            case "miniven":
              e = parseFloat(this.calculatorVarsProps.customsPriceMiniVan.val);
              break;
            case "heavy":
              e = parseFloat(this.calculatorVarsProps.customsPriceBigSuv.val);
              break;
            default:
              e = 0;
          }
          return console.log(e), e;
        },
        duty: function () {
          if (3 === this.fuelId) return 0;
          var e =
            "moto" === this.carType
              ? parseFloat(this.calculatorVarsProps.dutyMoto.val)
              : parseFloat(this.calculatorVarsProps.duty.val);
          return Math.round(
            (parseFloat(this.price) +
              this.getAuctionPrice +
              this.customsPrice) *
              e
          );
        },
        exciseTax: function () {
          var e = 0,
            t = 0,
            n = new Date().getFullYear() - this.carYear - 1;
          if ("moto" === this.carType) {
            for (
              var r = 0,
                a = this.calculatorVarsProps.exciseTaxMoto.conditional_data,
                i = 0;
              i < a.length;
              i++
            )
              parseFloat(this.volumeEngine) >= +a[i].from_condition &&
                parseFloat(this.volumeEngine) <= +a[i].to_condition &&
                (r = parseFloat(a[i].value));
            return Math.round(
              this.volumeEngine *
                parseFloat(this.calculatorVarsProps.exciseTaxMoto.val) *
                r
            );
          }
          return 3 === this.fuelId
            ? Math.round(
                parseFloat(this.calculatorVarsProps.exciseTaxElectro.val) *
                  this.volumeEngine
              )
            : ((e =
                1 === this.fuelId
                  ? 0 < this.volumeEngine &&
                    this.volumeEngine <
                      parseFloat(
                        this.calculatorVarsProps.baseExciseDieselLessThen
                          .condition.value
                      )
                    ? parseFloat(
                        this.calculatorVarsProps.baseExciseDieselLessThen.val
                      )
                    : parseFloat(this.calculatorVarsProps.baseExciseDiesel.val)
                  : 0 < this.volumeEngine &&
                    this.volumeEngine <
                      parseFloat(
                        this.calculatorVarsProps.baseExciseLessThen.condition
                          .value
                      )
                  ? parseFloat(this.calculatorVarsProps.baseExciseLessThen.val)
                  : parseFloat(this.calculatorVarsProps.baseExcise.val)),
              (t =
                n <
                  parseInt(
                    this.calculatorVarsProps.carYearLessThen.condition.value
                  ) && n >= 1
                  ? n
                  : n >=
                    parseInt(
                      this.calculatorVarsProps.carYearLessThen.condition.value
                    )
                  ? parseFloat(
                      this.calculatorVarsProps.carYearLessThen.condition.value
                    )
                  : 1),
              Math.round(e * t * (this.volumeEngine / 1e3)));
        },
        totalSum: function () {
          return parseFloat(this.price) > 0
            ? Math.round(
                parseFloat(this.price) +
                  this.getAuctionPrice +
                  this.portDelivery +
                  this.seaDeliveryPrice +
                  this.customsSumm +
                  this.broker +
                  this.expedit +
                  this.kyivDelivery +
                  this.cert +
                  this.register +
                  this.services +
                  this.insurance +
                  this.dangerCargo +
                  this.sublotPrice
              )
            : 0;
        },
      },
    });
